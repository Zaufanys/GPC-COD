"""
WZ Visual State for Gtuner IV Computer Vision.

This worker performs HUD/template classification only:
  - equipped weapon -> Titan recoil profile
  - optic family -> telemetry/reserved tuning input
  - UI context -> safe blocking of shared-input action helpers

It does not detect players, calculate target coordinates, or provide aim lock.

Gtuner IV entry point:
    class GCVWorker
    process(frame) -> (annotated_frame, bytearray)
"""

import glob
import json
import os
import struct
import time
from collections import deque

try:
    import cv2
except ImportError:  # Allows packet/config tests outside the Gtuner CV runtime.
    cv2 = None

try:
    import numpy as np
except ImportError:
    np = None


MAGIC = 0x575A
PROTOCOL_VERSION = 1
PACKET_FORMAT = "<HBBHHHBBBBBB"
PACKET_SIZE = struct.calcsize(PACKET_FORMAT)

FLAG_CAPTURE_OK = 1 << 0
FLAG_TEMPLATES_READY = 1 << 1
FLAG_UI_KNOWN = 1 << 2
FLAG_WEAPON_KNOWN = 1 << 3

UI_GAMEPLAY = 0
UI_REVIVE = 4
UI_PARACHUTE = 5
UI_UNKNOWN = 255
PROFILE_UNKNOWN = 255


def clamp_int(value, low, high):
    return max(low, min(high, int(value)))


def pack_packet(sequence, process_ms, capture_fps, weapon_id, optic_id,
                ui_state, confidence, profile, flags=0):
    """Pack the exact 16-byte little-endian contract consumed by wz.gpc."""
    return bytearray(struct.pack(
        PACKET_FORMAT,
        MAGIC,
        PROTOCOL_VERSION,
        clamp_int(flags, 0, 255),
        clamp_int(sequence, 0, 65535),
        clamp_int(round(process_ms), 0, 65535),
        clamp_int(round(capture_fps * 10.0), 0, 65535),
        clamp_int(weapon_id, 0, 255),
        clamp_int(optic_id, 0, 255),
        clamp_int(ui_state, 0, 255),
        clamp_int(round(confidence * 100.0), 0, 100),
        clamp_int(profile, 0, 255),
        0,
    ))


def load_config(base_dir):
    path = os.path.join(base_dir, "wz_cv_config.json")
    with open(path, "r", encoding="utf-8") as handle:
        config = json.load(handle)
    return config


def normalized_roi_to_pixels(roi, width, height):
    x1 = clamp_int(round(float(roi[0]) * width), 0, width - 1)
    y1 = clamp_int(round(float(roi[1]) * height), 0, height - 1)
    x2 = clamp_int(round(float(roi[2]) * width), x1 + 1, width)
    y2 = clamp_int(round(float(roi[3]) * height), y1 + 1, height)
    return x1, y1, x2, y2


class FpsMeter:
    def __init__(self, window=90):
        self.timestamps = deque(maxlen=max(2, int(window)))

    def tick(self, now):
        self.timestamps.append(now)

    @property
    def fps(self):
        if len(self.timestamps) < 2:
            return 0.0
        elapsed = self.timestamps[-1] - self.timestamps[0]
        if elapsed <= 0.0:
            return 0.0
        return (len(self.timestamps) - 1) / elapsed


class StableResult:
    def __init__(self, unknown_id, confirm_frames, hold_frames):
        self.unknown_id = int(unknown_id)
        self.confirm_frames = max(1, int(confirm_frames))
        self.hold_frames = max(0, int(hold_frames))
        self.current_id = self.unknown_id
        self.current_score = 0.0
        self.candidate_id = self.unknown_id
        self.candidate_count = 0
        self.miss_count = 0

    def update(self, candidate_id, score):
        candidate_id = int(candidate_id)
        score = float(score)

        if candidate_id == self.unknown_id:
            self.candidate_id = self.unknown_id
            self.candidate_count = 0
            self.miss_count += 1
            if self.miss_count > self.hold_frames:
                self.current_id = self.unknown_id
                self.current_score = 0.0
            return self.current_id, self.current_score

        self.miss_count = 0
        if candidate_id == self.candidate_id:
            self.candidate_count += 1
        else:
            self.candidate_id = candidate_id
            self.candidate_count = 1

        if self.candidate_count >= self.confirm_frames:
            self.current_id = candidate_id
            self.current_score = score
        return self.current_id, self.current_score


class TemplateClass:
    def __init__(self, base_dir, group_defaults, item):
        self.id = int(item["id"])
        self.name = str(item["name"])
        self.profile = int(item.get("profile", PROFILE_UNKNOWN))
        self.roi = item.get("roi", group_defaults["roi"])
        self.threshold = float(item.get(
            "threshold", group_defaults.get("threshold", 0.82)))
        self.method = str(item.get(
            "method", group_defaults.get("method", "edge"))).lower()
        self.target_size = item.get(
            "target_size", group_defaults.get("target_size", [256, 128]))
        patterns = item.get("templates", [])
        if isinstance(patterns, str):
            patterns = [patterns]
        self.paths = []
        for pattern in patterns:
            self.paths.extend(sorted(glob.glob(os.path.join(base_dir, pattern))))
        self.templates = []

    def load(self):
        if cv2 is None:
            return
        self.templates = []
        for path in self.paths:
            image = cv2.imread(path, cv2.IMREAD_COLOR)
            if image is None:
                continue
            self.templates.append(self.preprocess(image))

    def preprocess(self, image):
        width = max(16, int(self.target_size[0]))
        height = max(16, int(self.target_size[1]))
        resized = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        if self.method == "edge":
            gray = cv2.GaussianBlur(gray, (3, 3), 0)
            return cv2.Canny(gray, 60, 160)
        return cv2.equalizeHist(gray)

    def evaluate(self, frame):
        if not self.templates:
            return 0.0
        height, width = frame.shape[:2]
        x1, y1, x2, y2 = normalized_roi_to_pixels(
            self.roi, width, height)
        crop = frame[y1:y2, x1:x2]
        if crop.size == 0:
            return 0.0
        sample = self.preprocess(crop)
        best = 0.0
        for template in self.templates:
            score = float(cv2.matchTemplate(
                sample, template, cv2.TM_CCOEFF_NORMED)[0][0])
            if score > best:
                best = score
        return best


class DetectorGroup:
    def __init__(self, base_dir, config):
        self.name = str(config["name"])
        self.unknown_id = int(config.get("unknown_id", 0))
        self.check_every = max(1, int(config.get("check_every", 1)))
        self.classes = [
            TemplateClass(base_dir, config, item)
            for item in config.get("items", [])
        ]
        for item in self.classes:
            item.load()
        self.stable = StableResult(
            self.unknown_id,
            config.get("confirm_frames", 2),
            config.get("hold_frames", 3),
        )
        self.last_score = 0.0

    @property
    def template_count(self):
        return sum(len(item.templates) for item in self.classes)

    @property
    def every_class_has_template(self):
        return bool(self.classes) and all(
            len(item.templates) > 0 for item in self.classes)

    def item_by_id(self, item_id):
        for item in self.classes:
            if item.id == item_id:
                return item
        return None

    def evaluate(self, frame, classification_tick):
        if classification_tick % self.check_every:
            return self.stable.current_id, self.stable.current_score

        best_item = None
        best_score = 0.0
        for item in self.classes:
            score = item.evaluate(frame)
            if score >= item.threshold and score > best_score:
                best_item = item
                best_score = score

        candidate = self.unknown_id if best_item is None else best_item.id
        result = self.stable.update(candidate, best_score)
        self.last_score = result[1]
        return result


class WzVisualPipeline:
    def __init__(self, width, height, base_dir):
        if cv2 is None or np is None:
            raise RuntimeError(
                "WZ Visual State requires OpenCV and NumPy in Gtuner IV.")

        self.width = int(width)
        self.height = int(height)
        self.base_dir = base_dir
        self.config = load_config(base_dir)
        self.debug_overlay = bool(self.config.get("debug_overlay", True))
        self.target_process_fps = max(
            1.0, float(self.config.get("target_process_fps", 120.0)))
        self.min_classify_interval = 1.0 / self.target_process_fps
        self.next_classify_time = 0.0
        self.classification_tick = 0
        self.sequence = 0
        self.fps_meter = FpsMeter(self.config.get("fps_window", 90))

        groups = {
            group["name"]: DetectorGroup(base_dir, group)
            for group in self.config.get("groups", [])
        }
        self.weapon = groups.get("weapon")
        self.optic = groups.get("optic")
        self.ui = groups.get("ui")
        if self.weapon is None or self.ui is None:
            raise ValueError("Config must contain weapon and ui groups.")

        self.last_weapon = self.weapon.unknown_id
        self.last_weapon_score = 0.0
        self.last_optic = 0
        self.last_optic_score = 0.0
        self.last_ui = UI_UNKNOWN
        self.last_ui_score = 0.0
        self.last_process_ms = 0.0

    @property
    def templates_ready(self):
        # Weapon and UI templates are mandatory; optic templates are optional.
        return self.weapon.template_count > 0 and self.ui.every_class_has_template

    def classify(self, frame):
        self.classification_tick += 1
        self.last_weapon, self.last_weapon_score = self.weapon.evaluate(
            frame, self.classification_tick)

        if self.optic is not None and self.optic.template_count:
            self.last_optic, self.last_optic_score = self.optic.evaluate(
                frame, self.classification_tick)

        matched_ui, ui_score = self.ui.evaluate(
            frame, self.classification_tick)

        if matched_ui != self.ui.unknown_id:
            self.last_ui = matched_ui
            self.last_ui_score = ui_score
        elif self.last_weapon != self.weapon.unknown_id:
            # A confirmed weapon HUD plus no blocking UI match is the explicit
            # gameplay signature. Unknown weapon/UI combinations fail safe.
            self.last_ui = UI_GAMEPLAY
            self.last_ui_score = self.last_weapon_score
        else:
            self.last_ui = UI_UNKNOWN
            self.last_ui_score = 0.0

    def current_profile(self):
        item = self.weapon.item_by_id(self.last_weapon)
        if item is None:
            return PROFILE_UNKNOWN
        return item.profile

    def current_confidence(self):
        # The packet confidence gates automatic recoil-profile selection, so
        # weapon confidence takes priority. UI state is independently fail-safe.
        if self.last_weapon != self.weapon.unknown_id:
            return self.last_weapon_score
        if self.last_ui != UI_UNKNOWN:
            return self.last_ui_score
        return 0.0

    def flags(self):
        flags = FLAG_CAPTURE_OK
        if self.templates_ready:
            flags |= FLAG_TEMPLATES_READY
        if self.last_ui != UI_UNKNOWN:
            flags |= FLAG_UI_KNOWN
        if self.last_weapon != self.weapon.unknown_id:
            flags |= FLAG_WEAPON_KNOWN
        return flags

    def draw_overlay(self, frame):
        if not self.debug_overlay:
            return frame
        color = (40, 220, 40) if self.last_ui != UI_UNKNOWN else (40, 40, 230)
        weapon_item = self.weapon.item_by_id(self.last_weapon)
        weapon_name = "UNKNOWN" if weapon_item is None else weapon_item.name
        ui_item = self.ui.item_by_id(self.last_ui)
        if self.last_ui == UI_GAMEPLAY:
            ui_name = "GAMEPLAY"
        elif ui_item is None:
            ui_name = "UNKNOWN"
        else:
            ui_name = ui_item.name
        text_lines = [
            "WZ CV v1 | capture %.1f fps | process %.2f ms" %
            (self.fps_meter.fps, self.last_process_ms),
            "weapon %s %.0f%% | profile %s" %
            (weapon_name, self.last_weapon_score * 100.0,
             self.current_profile()),
            "ui %s %.0f%% | seq %d" %
            (ui_name, self.last_ui_score * 100.0, self.sequence),
        ]
        y = 28
        for line in text_lines:
            cv2.putText(frame, line, (18, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.62, (0, 0, 0), 3, cv2.LINE_AA)
            cv2.putText(frame, line, (18, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.62, color, 1, cv2.LINE_AA)
            y += 25
        return frame

    def process(self, frame):
        started = time.perf_counter()
        self.fps_meter.tick(started)

        if started >= self.next_classify_time:
            self.next_classify_time = started + self.min_classify_interval
            self.classify(frame)

        self.sequence = (self.sequence + 1) & 0xFFFF
        annotated = self.draw_overlay(frame)
        self.last_process_ms = (time.perf_counter() - started) * 1000.0
        packet = pack_packet(
            self.sequence,
            self.last_process_ms,
            self.fps_meter.fps,
            self.last_weapon,
            self.last_optic,
            self.last_ui,
            self.current_confidence(),
            self.current_profile(),
            self.flags(),
        )
        return annotated, packet


class GCVWorker:
    """Gtuner IV Computer Vision worker contract."""

    def __init__(self, width, height):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.pipeline = WzVisualPipeline(width, height, base_dir)

    def __del__(self):
        self.pipeline = None

    def process(self, frame):
        return self.pipeline.process(frame)

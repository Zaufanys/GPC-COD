import importlib.util
import json
import re
import struct
import tempfile
import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("wz_cv", PROJECT_DIR / "wz_cv.py")
WZ_CV = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(WZ_CV)
TOOL_SPEC = importlib.util.spec_from_file_location(
    "make_template", PROJECT_DIR / "tools" / "make_template.py")
MAKE_TEMPLATE = importlib.util.module_from_spec(TOOL_SPEC)
TOOL_SPEC.loader.exec_module(MAKE_TEMPLATE)


class PacketContractTests(unittest.TestCase):
    def test_packet_is_exactly_16_bytes_and_little_endian(self):
        packet = WZ_CV.pack_packet(
            sequence=513,
            process_ms=7,
            capture_fps=119.5,
            weapon_id=2,
            optic_id=3,
            ui_state=4,
            confidence=0.87,
            profile=1,
            flags=15,
        )
        self.assertEqual(len(packet), 16)
        values = struct.unpack(WZ_CV.PACKET_FORMAT, packet)
        self.assertEqual(values[0], 0x575A)
        self.assertEqual(values[1], 1)
        self.assertEqual(values[3], 513)
        self.assertEqual(values[5], 1195)
        self.assertEqual(values[6:11], (2, 3, 4, 87, 1))

    def test_ui_ids_match_gpc_contract(self):
        self.assertEqual(WZ_CV.UI_GAMEPLAY, 0)
        self.assertEqual(WZ_CV.UI_REVIVE, 4)
        self.assertEqual(WZ_CV.UI_PARACHUTE, 5)
        self.assertEqual(WZ_CV.UI_UNKNOWN, 255)

    def test_normalized_roi(self):
        self.assertEqual(
            WZ_CV.normalized_roi_to_pixels(
                [0.25, 0.25, 0.75, 0.75], 1920, 1080),
            (480, 270, 1440, 810),
        )


class ConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(PROJECT_DIR / "wz_cv_config.json", "r", encoding="utf-8") as f:
            cls.config = json.load(f)

    def test_required_groups_and_unique_ids(self):
        groups = {group["name"]: group for group in self.config["groups"]}
        self.assertIn("weapon", groups)
        self.assertIn("ui", groups)
        for group in groups.values():
            ids = [item["id"] for item in group["items"]]
            self.assertEqual(len(ids), len(set(ids)))

    def test_rois_are_normalized_and_nonempty(self):
        for group in self.config["groups"]:
            for item in group["items"]:
                roi = item.get("roi", group["roi"])
                self.assertEqual(len(roi), 4)
                self.assertTrue(all(0.0 <= value <= 1.0 for value in roi))
                self.assertLess(roi[0], roi[2])
                self.assertLess(roi[1], roi[3])

    def test_weapon_profiles_fit_gpc_profiles(self):
        weapon = next(
            group for group in self.config["groups"]
            if group["name"] == "weapon")
        for item in weapon["items"]:
            self.assertIn(item.get("profile", 255), (0, 1, 2, 255))

    def test_required_guard_ui_states_exist(self):
        ui = next(
            group for group in self.config["groups"]
            if group["name"] == "ui")
        ids = {item["id"] for item in ui["items"]}
        self.assertTrue({4, 5}.issubset(ids))

    def test_gpc_receiver_matches_packet_contract(self):
        source = (PROJECT_DIR / "wz.gpc").read_text(encoding="utf-8")
        self.assertIn("#define GCV_MAGIC              0x575A", source)
        self.assertIn("#define GCV_PROTOCOL_VERSION        1", source)
        self.assertIn("#define GCV_UI_REVIVE                4", source)
        expected_reads = {
            0: "cv_magic",
            2: "cv_version",
            3: "cv_flags",
            4: "cv_sequence",
            6: "cv_process_ms",
            8: "cv_capture_fps_x10",
            10: "cv_weapon_id",
            11: "cv_optic_id",
            12: "cv_ui_state",
            13: "cv_confidence",
            14: "cv_profile",
            15: "cv_reserved",
        }
        for offset, variable in expected_reads.items():
            self.assertIn(
                "gcv_read(%d, &%s);" % (offset, variable),
                source,
            )

    def test_gpc_uses_native_titan_two_apis(self):
        source = (PROJECT_DIR / "wz.gpc").read_text(encoding="utf-8")
        self.assertNotIn("get_rtime(", source)
        self.assertNotIn("combo_running(", source)
        self.assertNotIn("get_rumble(", source)
        for legacy_identifier in ("RUMBLE_A", "RUMBLE_B", "RUMBLE_RT", "RUMBLE_LT"):
            self.assertNotIn(legacy_identifier, source)
        self.assertIn("elapsed_time()", source)
        self.assertIn("ffb_get_actual(FFB_1, NULL)", source)
        self.assertIn("ffb_get_actual(FFB_4, NULL)", source)

    def test_template_output_directory_keeps_item_folder(self):
        weapon = next(
            group for group in self.config["groups"]
            if group["name"] == "weapon")
        fg42 = next(item for item in weapon["items"] if item["name"] == "FG42")
        output = MAKE_TEMPLATE.output_directory(PROJECT_DIR, fg42)
        self.assertEqual(
            output,
            PROJECT_DIR / "templates" / "weapons" / "fg42",
        )

    def test_gpc_interactive_config_offsets_do_not_overlap(self):
        source = (PROJECT_DIR / "wz.gpc").read_text(encoding="utf-8")
        blocks = re.findall(r"\[[^\]]+\]\n(?:[^\[]+?)(?=\n\[|</cfgdesc>)", source)
        ranges = []
        for block in blocks:
            offset = re.search(r"byteoffset\s*=\s*(\d+)", block)
            bitsize = re.search(r"bitsize\s*=\s*(\d+)", block)
            if not offset or not bitsize:
                continue
            start = int(offset.group(1))
            byte_count = int(bitsize.group(1)) // 8
            title = block.splitlines()[0]
            ranges.append((start, start + byte_count, title))

        seen = {}
        for start, end, title in ranges:
            for byte in range(start, end):
                self.assertNotIn(
                    byte,
                    seen,
                    "PMEM byte %d is shared by %s and %s" %
                    (byte, seen.get(byte), title),
                )
                seen[byte] = title

        self.assertIn(139, seen)

    def test_every_pmem_offset_has_a_cfgdesc_field(self):
        source = (PROJECT_DIR / "wz.gpc").read_text(encoding="utf-8")
        pmem_offsets = {
            int(value)
            for value in re.findall(r"#define\s+PM_[A-Z0-9_]+\s+(\d+)", source)
        }
        cfg_offsets = {
            int(value)
            for value in re.findall(r"byteoffset\s*=\s*(\d+)", source)
        }
        self.assertEqual(pmem_offsets, cfg_offsets)


class StableResultTests(unittest.TestCase):
    def test_requires_confirmation_and_holds_short_misses(self):
        stable = WZ_CV.StableResult(
            unknown_id=255,
            confirm_frames=2,
            hold_frames=1,
        )
        self.assertEqual(stable.update(4, 0.90)[0], 255)
        self.assertEqual(stable.update(4, 0.91)[0], 4)
        self.assertEqual(stable.update(255, 0.0)[0], 4)
        self.assertEqual(stable.update(255, 0.0)[0], 255)


@unittest.skipIf(WZ_CV.cv2 is None or WZ_CV.np is None, "OpenCV is not installed")
class VisualPipelineSmokeTests(unittest.TestCase):
    def test_pipeline_matches_synthetic_weapon_and_ui_templates(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            weapon_dir = base_dir / "templates" / "weapon"
            ui_dir = base_dir / "templates" / "ui"
            weapon_dir.mkdir(parents=True)
            ui_dir.mkdir(parents=True)

            frame = WZ_CV.np.zeros((120, 160, 3), dtype=WZ_CV.np.uint8)
            WZ_CV.cv2.rectangle(frame, (35, 25), (125, 95), (255, 255, 255), 4)
            WZ_CV.cv2.line(frame, (45, 80), (115, 40), (255, 255, 255), 3)
            WZ_CV.cv2.imwrite(str(weapon_dir / "sample.png"), frame)
            WZ_CV.cv2.imwrite(str(ui_dir / "sample.png"), frame)

            config = {
                "target_process_fps": 120,
                "debug_overlay": False,
                "groups": [
                    {
                        "name": "weapon",
                        "unknown_id": 0,
                        "roi": [0.0, 0.0, 1.0, 1.0],
                        "target_size": [64, 48],
                        "method": "edge",
                        "threshold": 0.8,
                        "check_every": 1,
                        "confirm_frames": 1,
                        "hold_frames": 0,
                        "items": [{
                            "id": 1,
                            "name": "TEST_WEAPON",
                            "profile": 0,
                            "templates": ["templates/weapon/*.png"],
                        }],
                    },
                    {
                        "name": "ui",
                        "unknown_id": 255,
                        "roi": [0.0, 0.0, 1.0, 1.0],
                        "target_size": [64, 48],
                        "method": "edge",
                        "threshold": 0.8,
                        "check_every": 1,
                        "confirm_frames": 1,
                        "hold_frames": 0,
                        "items": [{
                            "id": WZ_CV.UI_REVIVE,
                            "name": "REVIVE",
                            "templates": ["templates/ui/*.png"],
                        }],
                    },
                ],
            }
            (base_dir / "wz_cv_config.json").write_text(
                json.dumps(config),
                encoding="utf-8",
            )

            pipeline = WZ_CV.WzVisualPipeline(160, 120, str(base_dir))
            _, packet = pipeline.process(frame.copy())
            values = struct.unpack(WZ_CV.PACKET_FORMAT, packet)

            self.assertTrue(pipeline.templates_ready)
            self.assertEqual(pipeline.last_weapon, 1)
            self.assertEqual(pipeline.last_ui, WZ_CV.UI_REVIVE)
            self.assertEqual(pipeline.current_profile(), 0)
            self.assertTrue(values[2] & WZ_CV.FLAG_TEMPLATES_READY)
            self.assertTrue(values[2] & WZ_CV.FLAG_WEAPON_KNOWN)


if __name__ == "__main__":
    unittest.main()

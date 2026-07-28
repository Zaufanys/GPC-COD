import importlib.util
import json
import re
import struct
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

        self.assertIn(135, seen)


if __name__ == "__main__":
    unittest.main()

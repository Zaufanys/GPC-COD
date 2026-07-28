"""Crop a WZ CV template from a user-owned screenshot using config ROIs."""

import argparse
import glob
import json
import os
import sys
from pathlib import Path

from PIL import Image


def load_config(project_dir):
    with open(project_dir / "wz_cv_config.json", "r", encoding="utf-8") as handle:
        return json.load(handle)


def find_item(config, group_name, item_name):
    for group in config["groups"]:
        if group["name"].lower() != group_name.lower():
            continue
        for item in group.get("items", []):
            if item["name"].lower() == item_name.lower():
                return group, item
    raise KeyError("No config item %s/%s" % (group_name, item_name))


def output_directory(project_dir, item):
    patterns = item.get("templates", [])
    if isinstance(patterns, str):
        patterns = [patterns]
    if not patterns:
        raise ValueError("Config item has no template path.")
    pattern = patterns[0]
    wildcard_at = min(
        [index for index in (pattern.find("*"), pattern.find("?"))
         if index >= 0] or [len(pattern)]
    )
    prefix = pattern[:wildcard_at]
    if prefix.endswith(("/", "\\")):
        folder = prefix.rstrip("/\\")
    else:
        folder = os.path.dirname(prefix)
    return project_dir / folder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, help="Full capture screenshot")
    parser.add_argument("--group", required=True, choices=["weapon", "optic", "ui"])
    parser.add_argument("--item", required=True, help="Config item name")
    parser.add_argument("--suffix", default="", help="Optional filename suffix")
    args = parser.parse_args()

    project_dir = Path(__file__).resolve().parents[1]
    config = load_config(project_dir)
    group, item = find_item(config, args.group, args.item)
    roi = item.get("roi", group["roi"])

    image_path = Path(args.image).resolve()
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    x1 = max(0, min(width - 1, round(roi[0] * width)))
    y1 = max(0, min(height - 1, round(roi[1] * height)))
    x2 = max(x1 + 1, min(width, round(roi[2] * width)))
    y2 = max(y1 + 1, min(height, round(roi[3] * height)))
    crop = image.crop((x1, y1, x2, y2))

    destination = output_directory(project_dir, item)
    destination.mkdir(parents=True, exist_ok=True)
    existing = glob.glob(str(destination / "*.png"))
    suffix = ("-" + args.suffix.strip()) if args.suffix.strip() else ""
    filename = "%s-%03d%s.png" % (
        item["name"].lower(), len(existing) + 1, suffix)
    output = destination / filename
    crop.save(output)
    print(output)
    print("ROI pixels: %d,%d to %d,%d from %dx%d" %
          (x1, y1, x2, y2, width, height))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("error:", exc, file=sys.stderr)
        raise SystemExit(1)

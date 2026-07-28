"""Benchmark WZ CV processing against one or more captured screenshots."""

import argparse
import statistics
import sys
import time
from pathlib import Path

import cv2

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from wz_cv import WzVisualPipeline  # noqa: E402


def percentile(values, fraction):
    ordered = sorted(values)
    index = min(len(ordered) - 1, round((len(ordered) - 1) * fraction))
    return ordered[index]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("images", nargs="+")
    parser.add_argument("--loops", type=int, default=200)
    args = parser.parse_args()

    frames = []
    for path in args.images:
        frame = cv2.imread(path, cv2.IMREAD_COLOR)
        if frame is None:
            raise SystemExit("Could not load %s" % path)
        frames.append(frame)

    height, width = frames[0].shape[:2]
    worker = WzVisualPipeline(width, height, str(PROJECT_DIR))
    timings = []
    for index in range(max(1, args.loops)):
        frame = frames[index % len(frames)].copy()
        started = time.perf_counter()
        worker.process(frame)
        timings.append((time.perf_counter() - started) * 1000.0)

    print("frames=%d loops=%d" % (len(frames), len(timings)))
    print("mean_ms=%.3f p50_ms=%.3f p95_ms=%.3f max_ms=%.3f" % (
        statistics.mean(timings),
        percentile(timings, 0.50),
        percentile(timings, 0.95),
        max(timings),
    ))
    print("equivalent_fps=%.1f" % (1000.0 / statistics.mean(timings)))


if __name__ == "__main__":
    main()


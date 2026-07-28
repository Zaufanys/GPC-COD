"""Controller stick event timing and centre-stability comparison tool.

Reports SDL/Pygame-visible events: useful for direct-controller versus Titan-path
comparison, but not proof of raw USB hardware polling.
"""
from __future__ import annotations
import argparse
import statistics
import time

def summary(points):
    intervals = [(b - a) / 1_000_000 for a, b in zip(points, points[1:]) if b > a]
    if not intervals:
        return None
    values = sorted(intervals)
    return len(values), statistics.median(values), values[min(len(values)-1, round((len(values)-1)*.95))], values[0], values[-1]

def suggested_deadzone(samples):
    return min(12.0, max(2.0, max((abs(x) for x in samples), default=0.0) * 100 + 1.0))

def pygame_module():
    try:
        import pygame
        return pygame
    except ImportError as exc:
        raise SystemExit("Install first: py -m pip install -r requirements-diagnostics.txt") from exc

def list_devices(pg):
    pg.joystick.init()
    if not pg.joystick.get_count():
        print("No SDL controller detected. Connect it directly, then rerun.")
    for index in range(pg.joystick.get_count()):
        joy = pg.joystick.Joystick(index); joy.init()
        print(f"[{index}] {joy.get_name()} | axes={joy.get_numaxes()} | guid={joy.get_guid()}")

def open_device(pg, index):
    pg.joystick.init()
    if index < 0 or index >= pg.joystick.get_count():
        raise SystemExit("Invalid device index. Run with --list first.")
    joy = pg.joystick.Joystick(index); joy.init()
    return joy

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--right-x", type=int, default=2)
    parser.add_argument("--right-y", type=int, default=3)
    parser.add_argument("--duration", type=float, default=10.0)
    parser.add_argument("--threshold", type=float, default=.003)
    parser.add_argument("--monitor", action="store_true")
    args = parser.parse_args()
    pg = pygame_module(); pg.init()
    try:
        if args.list:
            list_devices(pg); return
        joy = open_device(pg, args.device)
        if min(args.right_x, args.right_y) < 0 or max(args.right_x, args.right_y) >= joy.get_numaxes():
            raise SystemExit(f"Device has {joy.get_numaxes()} axes; use --monitor to find the right stick.")
        if args.monitor:
            print("Move sticks; Ctrl+C stops.")
            while True:
                pg.event.pump()
                print("\r" + " ".join(f"A{i}={joy.get_axis(i):+.3f}" for i in range(joy.get_numaxes())), end="", flush=True)
                time.sleep(.05)
        print("Keep the right stick still for 3 seconds.")
        centre = []; until = time.perf_counter() + 3
        while time.perf_counter() < until:
            pg.event.pump(); centre += [joy.get_axis(args.right_x), joy.get_axis(args.right_y)]; time.sleep(.002)
        print(f"Sweep right stick smoothly left/right and up/down for {args.duration:.0f} seconds; axes are measured separately.")
        previous = {args.right_x: joy.get_axis(args.right_x), args.right_y: joy.get_axis(args.right_y)}
        points = {args.right_x: [], args.right_y: []}; until = time.perf_counter() + args.duration
        while time.perf_counter() < until:
            for event in pg.event.get():
                if event.type == pg.JOYAXISMOTION and event.axis in previous and abs(event.value - previous[event.axis]) >= args.threshold:
                    points[event.axis].append(time.perf_counter_ns()); previous[event.axis] = event.value
        print(f"\nDevice: {joy.get_name()} ({joy.get_guid()})")
        print(f"Centre max: {max((abs(x) for x in centre), default=0):.4f}")
        print(f"Suggested WZ Core ADS inner response deadzone: {suggested_deadzone(centre):.1f}")
        captured = False
        for axis, label in ((args.right_x, "X"), (args.right_y, "Y")):
            result = summary(points[axis])
            if result:
                captured = True
                n, median, p95, low, high = result
                print(f"Axis {label} (A{axis}): n={n}, median={median:.3f} ms (~{1000/median:.1f} Hz), p95={p95:.3f} ms, min={low:.3f} ms, max={high:.3f} ms")
        if not captured:
            print("No meaningful events captured. Check axes with --monitor.")
        print("SDL-visible estimate only; compare repeated direct-PC and Titan-path runs.")
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        pg.quit()

if __name__ == "__main__":
    main()

# Performance and Latency

## Your PC setup

For a 200+ FPS Warzone render rate, 220 Hz monitor, and 1000 Hz controller/Titan input-output:

- Keep Titan Two input and output polling at **1000 Hz**.
- The GPC2 main loop passes raw controller input every device cycle. Aim pattern intervals and combo waits schedule optional output; they do not reduce the controller polling rate.
- Set `target_process_fps` in `wz_cv_config.json` to the **actual capture feed rate**, not the Warzone render FPS or monitor refresh rate.

Recommended values:

| Capture feed | `target_process_fps` | GCV stale timeout |
|---|---:|---:|
| 60 FPS | 60 | 100–150 ms |
| 120 FPS | 120 | 50–100 ms |
| 144 FPS | 144 | 40–80 ms |
| 240 FPS | 240 | 25–60 ms |

Do not select 220 or 240 unless the capture source actually delivers that rate to Gtuner. A 220 Hz monitor does not automatically give Computer Vision 220 frames per second.

## Latency budget

The visual path is separate from the 1 ms controller path:

```text
game frame
  -> capture/transfer/buffering
  -> Gtuner frame delivery
  -> ROI template classification
  -> 16-byte GCV packet
  -> next Titan loop
```

Approximate frame periods:

| Feed | One frame |
|---|---:|
| 60 FPS | 16.67 ms |
| 120 FPS | 8.33 ms |
| 144 FPS | 6.94 ms |
| 240 FPS | 4.17 ms |

Total latency is the frame wait plus capture buffering/transfer, classifier processing, Gtuner delivery, and up to roughly one Titan polling interval. The debug overlay reports capture FPS and processing time, but it cannot measure capture-card buffering by itself.

## Fast-path design

- UI matching uses cropped regions resized to at most 320×180.
- Weapon matching runs every second classification tick by default.
- Optic matching runs every fourth tick.
- No neural-network runtime is loaded.
- No sleep or blocking wait is used in the GCV worker.
- The Titan consumes only a 16-byte packet and ignores stale or low-confidence profile results.
- Stale visual data blocks only optional action helpers; it never blocks raw controller input.

## Benchmark

After adding templates and installing OpenCV:

```powershell
py tools\benchmark_cv.py captures\gameplay.png captures\buy-station.png --loops 500
```

For a 120 FPS capture target, aim for classifier p95 below 8.33 ms. For 240 FPS, aim for p95 below 4.17 ms. If it is slower:

1. Reduce the number of templates per class.
2. Reduce `target_size` for the slow group.
3. Increase `check_every` for weapon or optic detection.
4. Keep UI detection at every classification tick because it is the safety guard.

## Display path

Avoid routing the 220 Hz gameplay display through hardware or software that caps the passthrough below 220 Hz. Use a capture path that preserves the primary display timing, then verify the actual Gtuner capture FPS in the WZ CV overlay.


# Controller response diagnostic

`tools/controller_response_test.py` measures controller events visible to Windows through SDL/Pygame and samples right-stick centre stability. It is a comparison tool, not a USB protocol analyser: it cannot certify the SCUF's raw hardware polling rate.

## Direct controller test

1. Connect the SCUF Valor Pro directly to the PC by USB. Do not route it through Titan Two for this first pass.
2. Enable the controller's wired-PC 1K mode if supported by its current SCUF firmware/software.
3. Close Steam Input and other remappers while measuring.
4. From the `wz` folder:

   ```powershell
   py -m pip install -r requirements-diagnostics.txt
   py tools\controller_response_test.py --list
   py tools\controller_response_test.py --device 0 --monitor
   ```

5. Identify the right-stick axes (often 2 and 3), then run:

   ```powershell
   py tools\controller_response_test.py --device 0 --right-x 2 --right-y 3
   ```

The first three seconds measure centre stability. Then make smooth continuous right-stick circles for ten seconds. Run three times and compare the *median* and p95 interval; a single maximum normally includes Windows scheduling delay.

## Titan-path comparison

Repeat after routing through Titan Two and select the virtual Xbox/controller device exposed to Windows. That measures the **effective Windows-visible path**. It cannot reveal the raw upstream SCUF report rate inside Titan Two, which is why generic polling tools may show no result or only the virtual device.

Keep cable, USB port, axes, duration, and background applications the same. Set Gtuner input/output to the same intended rate (for example, 1000 Hz) before the Titan-path run.

## TMR right-stick softening

WZ Core v0.4 adds Interactive Configuration entries:

| Setting | Start | Effect |
|---|---:|---|
| ADS Stick Softening | Off | Enables ADS-only response shaping; hip aim remains raw. |
| ADS Inner Response Deadzone | 2.0–3.0 | Removes tiny centre movement/drift. |
| ADS Soft-Curve Strength | 40–55 | Makes small/medium movements less abrupt while keeping full-stick speed. |

It is software response shaping only: it cannot reduce physical TMR spring force and adds no scheduled delay. Start at `2.5` and `45`; lower Soft-Curve Strength first if initial ADS movement feels too slow. The script shape stacks with Warzone's own curve, so recalibrate recoil after a change.

## References

- [SCUF Valor Pro 1K polling setup](https://www.scufgaming.com/us/en/gaming/products/xbox-series-xs/how-to-enable-1k-polling-on-scuf-valor-pro/)
- [SCUF polling-rate explanation](https://www.scufgaming.com/us/en/gaming/products/scuf-products/controller-polling-rate-explained/)
- [Pygame joystick event documentation](https://www.pygame.org/docs/ref/joystick.html)

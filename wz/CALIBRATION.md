# Calibration

## Recoil profiles

Keep the exact weapon build, optic, sensitivity, ADS multiplier, response curve, deadzones, FOV, and platform unchanged while calibrating.

1. Set all three vertical, horizontal, and first-shot values to 0.
2. In a practice environment, fire a full magazine at a fixed wall point without touching the right stick.
3. Enable Dynamic Anti-Recoil and raise the selected profile's vertical value in small 1.0 steps.
4. Correct consistent sideways drift with horizontal value. Positive and negative direction depends on the observed drift.
5. Tune first-shot boost only after sustained vertical/horizontal compensation is stable.
6. Repeat at the range you actually use the build.
7. Save one exact build per profile and retest after any Warzone weapon patch.

Do not copy a percentage from patch notes into the Titan value. An 8% base-recoil reduction does not mean the correct stick compensation is 8.

## CV templates

Use screenshots from the same feed Gtuner will analyze:

- same resolution and aspect ratio
- same HUD scale and language
- same color/contrast/HDR path
- same capture device and processing

Capture at least three examples for every UI state and each weapon you want automatically selected. Use different backgrounds but keep the relevant HUD element clear.

```powershell
py tools\make_template.py --image captures\fg42-01.png --group weapon --item FG42
py tools\make_template.py --image captures\parachute-01.png --group ui --item PARACHUTE
```

Start with the configured 0.82 weapon and 0.80 UI thresholds:

- false match: raise that item's threshold by 0.02
- correct state missed: add more templates before lowering the threshold
- unstable weapon swap: increase weapon `confirm_frames`
- slow UI blocking: keep UI `check_every` at 1 and reduce only the ROI/target size

## Validation order

1. Run the Python unit tests.
2. Run the CV worker with debug overlay and GCV disabled in the GPC menu.
3. Verify templates and confidence.
4. Enable GCV Visual State Input and Context Guard.
5. Test stale behavior by stopping the CV worker; action helpers should stop while raw input continues.
6. Enable automatic recoil profile selection.
7. Enable one gameplay helper at a time.


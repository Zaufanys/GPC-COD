# WZ

Native Titan Two / GPC2 Warzone project with a Gtuner IV Interactive Configuration menu.

Current milestone: `v0.1-foundation`

## Included

- Four explicit aim micro-motion engines: Polar, Shake, Velocity, and Sticky
- Optional left-stick rotational micro-motion
- Three manual dynamic anti-recoil profiles with first-shot boost
- Auto tactical sprint fallback
- Boosted Sprint Refresh mode for periodic sprint/tactical-sprint re-input
- Slide-to-jump and slide-to-stand sequences
- Snake lateral movement, retained from the supplied script concept
- Guarded fast-loot pulse, plate hold assist, and parachute cut/redeploy cycle
- Quick Revive Hold Assist using a separate D-Pad Up + Use/Reload chord
- Rumble Profile Hint fallback for calibrated recoil-profile selection
- Runtime Context Lock for Buy Stations, loadouts, inventory, revives, and other shared-input screens
- A 16-byte stale-safe GCV protocol
- Fast ROI/template classification for weapon, optic, and UI state
- Template calibration and latency benchmark tools
- All gameplay-altering modules default **Off**

The project intentionally does **not** call any controller-only behavior “Aim Lock.” Without video analysis there is no target position, weapon identity, shop state, parachute state, or revive state in ordinary controller input. Names such as AA V2/V3/V5, Pro Aim, Batts Sticky Aim, and Enhanced Tracking are vendor labels rather than shared technical standards. See [LAB_FEATURES.md](LAB_FEATURES.md) for the re-added lab notes on speed, revive, rumble, and target/aim-lock boundaries.

## Install

1. Open `wz.gpc` in Gtuner IV.
2. Compile it with the GPC2 compiler.
3. Program it to a Titan Two memory slot.
4. Open **Interactive Configuration** for that slot.
5. Leave every module Off at first, then test one module at a time.

Default mapping is the standard Xbox/PlayStation controller layout. Tactical layouts and remapped buttons need a mapping layer in the next milestone.

## Recommended Warzone settings

- Sprint Assist: **Tactical Sprint Assist**
- Sprint Assist Delay: **0**
- Armor Plate Behavior: **Apply All**
- Slide behavior: use a tap/hybrid option that matches the selected script sequence
- Verify Interact/Reload Behavior before enabling Fast Loot

The native game settings are preferred where they already solve the problem. The script fallback exists for setups where the native behavior does not fit.

## Runtime controls

| Control | Action |
|---|---|
| ADS + D-Pad Right | Next recoil profile |
| ADS + D-Pad Left | Previous recoil profile |
| ADS + D-Pad Down | Toggle Context Lock |
| D-Pad Down + Stance | Snake, when enabled |
| D-Pad Left + Use/Reload | Guarded fast-loot pulse, when enabled |
| D-Pad Left + Swap/Plate | Plate hold assist, when enabled |
| D-Pad Left + Jump | Parachute cut/redeploy cycle, when enabled |
| D-Pad Up + Use/Reload | Quick Revive Hold Assist, when enabled |

Context Lock disables movement and action helpers. It does not change aim or anti-recoil.

## PC / 1000 Hz setup

Your Warzone frame rate, monitor refresh, Titan polling rate, and CV capture rate are separate:

- Keep Gtuner input and output at **1000 Hz** for the 1 ms controller path.
- Keep Warzone uncapped or capped appropriately for the 220 Hz display.
- Set `target_process_fps` in `wz_cv_config.json` to the capture feed's real rate. Use 120 only for a real 120 FPS feed; do not set it to 200 or 220 merely because the game/monitor runs that fast.
- The GPC2 script never waits before passing physical input. Its timed patterns run as optional scheduled outputs.

See [PERFORMANCE.md](PERFORMANCE.md) for capture-rate targets, latency budget, and benchmarking.
See [RESEARCH_2026.md](RESEARCH_2026.md) for the feature/recoil findings and [CALIBRATION.md](CALIBRATION.md) for the tuning workflow.

## Visual capture setup

1. In Gtuner IV, install/enable its Computer Vision Python and OpenCV support.
2. Select the capture source and verify its real frame rate.
3. Add screenshots from that exact feed to a local `captures` folder.
4. Create at least three templates per state:

   ```powershell
   py tools\make_template.py --image captures\fg42-01.png --group weapon --item FG42
   py tools\make_template.py --image captures\buy-01.png --group ui --item BUY_STATION
   ```

5. Repeat for the weapon, optic, and UI entries you use. Template folders are documented in [templates/README.md](templates/README.md).
6. Load `wz_cv.py` in Gtuner IV Computer Vision.
7. Confirm the overlay reports the right weapon/UI with stable confidence.
8. In the script's Interactive Configuration, enable **GCV Visual State Input**, then **GCV Context Guard**. Enable automatic recoil-profile switching only after weapon detection is reliable.

The repository cannot ship universal screenshots: HUD scale, resolution, language, color filters, capture processing, optic, and weapon build all change the pixels. Calibration from your exact feed is what makes detection accurate.

The CV worker intentionally detects HUD state only. It does not detect players or generate target-stick coordinates. The lab notes explain how to keep any target-detection experiments separated from the live Titan output contract.

## Current Season 05 recoil notes

The July 22, 2026 official Season 05 patch notes provide relative recoil changes, not controller-stick compensation values:

- **FG42:** new full-auto AR with an open-bolt delay. Its MFS Ambilateral Stock removes nearly all horizontal recoil but introduces aggressive vertical recoil.
- **AN-94:** base recoil reduced by about 8% in Battle Royale and Resurgence.
- **Voyak KT-3:** base recoil reduced by 5% in Battle Royale and Resurgence.
- **Swordfish A1 + MFS Penta Burst:** recoil increased, especially first-shot recoil.

For that reason the three profile defaults are neutral. Correct Titan values depend on the exact build, optic, sensitivity, response curve, deadzones, FOV, and platform. The planned GCV layer will identify weapon/optic state and select a calibrated profile; it will not invent compensation from patch-note percentages.

Sources:

- [Warzone Season 05 patch notes](https://www.callofduty.com/patchnotes/2026/07/call-of-duty-bo7-warzone-season-05-patch-notes)
- [Warzone Season 05 content announcement](https://www.callofduty.com/blog/2026/07/call-of-duty-black-ops-7-warzone-season-05-announcement)
- [Gtuner IV](https://www.consoletuner.com/software/gtuner-iv/)

## Important limitations

- A script cannot raise Warzone's movement-speed cap. “Boosted Sprint Refresh” periodically re-sends sprint/tactical-sprint input only.
- A script cannot shorten a server-controlled revive timer. Quick Revive Hold Assist only holds the normal input, and with GCV guard enabled it requires a fresh REVIVE UI match.
- Fast Loot cannot be fully context-safe from controller data alone. Use the guarded chord and Context Lock; the optional GCV guard adds UI-aware blocking after calibration.
- With GCV disabled, parachute state is not present in controller data and the cut/redeploy sequence is manual. With GCV enabled, the explicit chord is accepted only on a fresh parachute-state match.
- Rumble Profile Hint is a fallback profile selector, not reliable weapon identification. GCV weapon detection wins whenever it is fresh and confident.

Activision states that unauthorized scripted input devices are prohibited and subject to detection/enforcement. Review the current policy before using this project online: [RICOCHET Anti-Cheat Season 04 update](https://www.callofduty.com/blog/2026/06/call-of-duty-black-ops-7-warzone-ricochet-anti-cheat-season-04).

## Hardware validation checklist

- Compile `wz.gpc` in the installed Gtuner IV version.
- Confirm the default controller layout or add the mapping layer for a tactical/custom layout.
- Verify each combo in a practice environment because Warzone timing can change by patch.
- Calibrate weapon recoil values for the exact build, sensitivity, response curve, deadzones, FOV, and optic.
- Run `tools\benchmark_cv.py` and compare p95 processing time with the capture frame period.
- Tune template thresholds from the debug confidence overlay.

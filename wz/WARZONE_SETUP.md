# Warzone and Titan Two Setup

Checked for the Black Ops 7 Warzone rules in effect on 2026-07-28.

The safest configuration is to let Warzone handle movement natively and leave
the script's sprint fallback Off. Use the fallback only if native Sprint Assist
is unreliable with the specific controller/input path.

## Recommended native movement profile

Menu labels can vary slightly by update, but use the equivalent settings:

| Warzone setting | Recommended value | Why |
|---|---|---|
| Sprint Assist | On / Sprint Assist | Native movement has the fewest input conflicts |
| Sprint Assist Delay | 0 | Starts sprint without an artificial delay |
| Sprint Assist Sideways | On, if available | Supports lateral/omnimovement entry |
| Sprint Assist Backward | On, if available | Supports backward/omnimovement entry |
| Sprint Restore | On | Resumes sprint after allowed actions |
| Slide Maintains Sprint | On | Keeps movement flow after a slide |
| Slide/Dive Behavior | Tap to Slide | Most predictable match for the script's slide sequences |
| Slide/Dive Action Delay | Short | Reduces accidental dive while keeping the tap distinction |
| Mantle Assist | Off | Reduces unintended automatic mantles |
| Crouch Assist | Off | Avoids fighting manual/script stance input |
| Armor Plate Behavior | Apply All | More reliable than a scripted repeated plate sequence |
| Interact/Reload Behavior | Prioritize Interact | Best match for guarded loot pulses; reload becomes a hold |
| ADS Behavior | Hold | Matches the script's ADS gates |
| Controller Vibration | Off normally; On only for Rumble Profile Hint | Rumble selection has no signal if vibration is disabled |

Tactical sprint is not a universal base ability in current Warzone. It requires
the **Sprinter perk**. Without that perk, a double-tap or refresh can only
re-trigger normal sprint.

## When using Sprint Re-trigger / Boosted Refresh

To test the script-managed sprint path cleanly:

1. Set Warzone Sprint Assist to **Off**.
2. Enable **Script Sprint Fallback** in Interactive Configuration.
3. Select **Sprint Re-trigger / Boosted Refresh**.
4. Start with a **900 ms** re-trigger time.
5. Keep **Sprint Forward Threshold** at **92.0** if Device Monitor shows the
   left stick reaches at least `-92` to `-100` on `STICK_2_Y`.
6. If the stick does not consistently cross `-92`, lower the threshold gradually
   to **88.0**, then **85.0**. Do not lower it so far that ordinary walking
   triggers sprint.

The hardened v0.2 behavior sends a double tap immediately when full-forward
movement begins. Press and Double Tap modes trigger once per forward-stick
engagement. Re-trigger mode sends the initial double tap and then repeats only
at the configured interval.

Do not combine native automatic Sprint Assist with the script fallback during
calibration. Once both paths are individually verified, native Sprint Assist is
still the preferred final setup.

## Script feature compatibility

| Script feature | Required or recommended game setting |
|---|---|
| Slide to Jump / Stand | Tap to Slide; Slide Maintains Sprint On |
| Plate Hold Assist | Armor Plate Behavior Apply All |
| Fast Loot Pulse | Prioritize Interact; safer D-Pad Left chord only |
| Parachute Cut Cycle | Standard stance/crouch cuts parachute; standard jump deploys |
| Quick Revive Hold | Standard Use/Reload bind; GCV Context Guard recommended |
| Rumble Profile Hint | Controller Vibration On |
| Anti-Recoil profiles | Do not change sensitivity, ADS multiplier, curve, FOV, deadzones, optic, or build after calibration |

## Controller and deadzones

- Use the lowest left/right minimum deadzones that do not drift.
- Confirm both sticks reach their full range in Gtuner Device Monitor.
- The sprint helper reads physical `STICK_2_Y`; forward must cross the configured
  negative threshold.
- Keep the standard mappings expected by `wz.gpc`, or ensure the Input Translator
  produces the same universal Titan button/stick indexes.
- Paddle remaps should remain controller-side and resolve to Jump/Stance before
  the script receives them.

## Titan Two and PC

- Titan input polling: **1000 Hz**
- Titan output polling: **1000 Hz**
- Output protocol: use the XInput/Xbox protocol that Warzone detects correctly
  on the PC, and verify every control in Device Monitor before loading the script.
- Game FPS, monitor refresh, Titan polling, and GCV capture FPS are independent.
- Set `target_process_fps` to the capture source's real delivered rate, not the
  game's 200+ FPS or the monitor's 220 Hz.

## Safe validation order

1. Compile `wz.gpc` in Gtuner IV and program it with all optional modules Off.
2. Verify raw buttons, triggers, and both sticks in Device Monitor.
3. Enable one movement helper and test it in the firing range/private match.
4. Test Context Lock before opening shops, loadouts, or inventory.
5. Add and validate GCV templates before enabling GCV Context Guard.
6. Test revive and parachute states with the visual overlay visible.
7. Calibrate one exact recoil profile at a time.
8. Enable aim micro-motion only after the raw controller and recoil profile are
   stable; start with low radius and stop if it worsens manual control.

No static code audit can replace steps 1–8 because the final behavior depends on
the installed Gtuner compiler, firmware, controller reports, in-game bindings,
capture feed, and current Warzone timing.

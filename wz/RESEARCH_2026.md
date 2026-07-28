# Research Notes — Warzone Season 05, checked 2026-07-28

## What the popular aim labels actually mean

Most advertised names are not separate game APIs:

- **Polar, spiral, micro-circle, Sticky, Batts Sticky, AA V2/V3/V5:** timed right-stick micro-motion patterns or presets.
- **Enhanced Rotational AA:** small left-stick input intended to keep movement-based in-game assistance active.
- **Velocity Aim:** a useful technical distinction when the injected micro-pattern scales with physical stick speed.
- **Shake Aim:** alternating stick input; easy to implement, but frequently worse for precision.
- **Enhanced Tracking / Pro Aim:** marketing labels unless the implementation defines a measurable algorithm.
- **Aim Lock:** not possible from controller input alone because there are no target coordinates. Visual target detection is kept as a lab-only boundary in this project and is not wired to live Titan stick output.
- **Aim Abuse:** usually ADS cycling or other repeated activation. It conflicts with normal ADS timing and is excluded.

The project consolidates these names into four explicit, testable right-stick algorithms and one optional left-stick rotational algorithm.

## Action and movement feasibility

| Idea | Finding |
|---|---|
| Boosted sprint | A controller script can initiate or refresh sprint, but it cannot raise the game/server movement-speed cap. Tactical sprint requires the Sprinter perk in current Warzone. |
| Script sprint fallback | Viable, but Warzone's native Sprint Assist with delay 0 is the first choice. |
| Slide sequences | Viable, patch-sensitive, and dependent on the in-game slide/dive behavior. |
| Snake | Viable as an explicit lateral pattern; it should not silently alter normal movement. |
| Fast loot | Risky because Use/Reload is also used for reloads, loadouts, shops, and revives. It needs a chord, hold threshold, manual Context Lock, and optional CV guard. |
| Plate up | Native Armor Plate Behavior: Apply All is more reliable. A script hold is optional. |
| Quick revive | A script can hold the input but cannot shorten the server-controlled revive timer. WZ re-adds this as an explicit hold assist with a separate chord. |
| Rumble weapon ID | Rumble is usable as a rough fallback profile hint, but it is not stable enough to be the main weapon detector. |
| Parachute cut/redeploy | A manual sequence is viable. Automatic state awareness needs video because ordinary controller data has no parachute state. |

Season 05 also changes the loot flow with Supply Drones and airborne Buy Station deliveries, which makes conservative shared-input handling more important. [Official Season 05 patch notes](https://www.callofduty.com/patchnotes/2026/07/call-of-duty-bo7-warzone-season-05-patch-notes)

The current movement model removed tactical sprint as a universal base ability
and grants it through the Sprinter perk. [Official Warzone Season 01 movement notes](https://www.callofduty.com/patchnotes/2025/12/call-of-duty-bo7-warzone-season-01-patch-notes)

## Current recoil facts

The official July 22 Season 05 notes state:

- FG42 MFS Ambilateral Stock removes nearly all horizontal recoil but adds aggressive vertical recoil.
- AN-94 base recoil is reduced by about 8% in Battle Royale/Resurgence.
- Voyak KT-3 base recoil is reduced by 5% in Battle Royale/Resurgence.
- Swordfish A1 MFS Penta Burst recoil is increased, particularly first-shot recoil.

Those are relative tuning changes, not universal Titan values. Absolute compensation changes with attachment build, optic, sensitivity, response curve, deadzones, FOV, and platform. The project therefore uses neutral defaults and a calibration workflow instead of fabricated “season recoil numbers.”

## Titan/Gtuner implementation findings

- Gtuner IV officially supports a GPC2 compiler, Interactive Configuration, Device Monitor, and Python/OpenCV Computer Vision. [Gtuner IV overview](https://www.consoletuner.com/software/gtuner-iv/)
- Titan Two's documented Computer Vision integration can send analyzed capture data to GPC2. [Titan Two product capabilities](https://www.consoletuner.com/products/titan-two/)
- `gcv_ready()` must be checked before `gcv_read()`, reflected in the current Gtuner changelog and the receiver implementation. [Gtuner IV downloads/changelog](https://www.consoletuner.com/titan-two-downloads/)
- Public GCV examples prove the worker contract and binary feedback path, but older full-frame neural detectors are unnecessary for HUD state. This project uses small ROIs and templates for lower latency. [PhantomCV reference](https://github.com/BradyMeighan/PhantomCV)

## Compliance note

Activision's June 4, 2026 RICOCHET update says unauthorized scripted input devices are prohibited and that detection/enforcement continues. The project does not include detection evasion, random “humanization,” or claims that a pattern is safe from enforcement. [RICOCHET Season 04 update](https://www.callofduty.com/blog/2026/06/call-of-duty-black-ops-7-warzone-ricochet-anti-cheat-season-04)

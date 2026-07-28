# WZ Feature Matrix — 2026-07-27

This matrix compares the supplied Zen-era ideas with the first native Titan Two/GPC2 architecture.

| Feature or label | Decision | v0.1 implementation | Reason |
|---|---|---|---|
| Snake | Keep and simplify | Explicit D-Pad Down + Stance lateral pattern | Retains the supplied concept without silently altering normal movement |
| Boosted Sprint | Rename and constrain | Auto tactical sprint fallback | Titan can initiate sprint sooner but cannot exceed game movement speed |
| Auto Tactical Sprint | Keep | Press or double-tap modes | Viable, though the native Tactical Sprint Assist + delay 0 setting is preferred |
| Slide Sequences | Keep and update | Slide-to-jump and slide-to-stand | Old fixed slide-cancel timings are patch-sensitive |
| Parachute “plugging” | Add as manual prototype | Cut, configurable freefall, redeploy | No controller-only airborne state; automatic activation requires GCV |
| Plate Up | Prefer native; optional helper | Explicit chord and configurable hold | Apply All already handles the common case with less conflict |
| Fast Loot Pickup | Add with guardrails | Hold threshold, safer chord, ADS/fire block, Context Lock | Use/reload also controls loadouts, shops, reloads, and revives |
| Quick Revive | Reject speed claim | Not implemented | Input automation cannot shorten a server-controlled revive timer |
| Dynamic Anti-Recoil | Keep and rebuild | Three profiles, vertical/horizontal, first-shot boost | Useful architecture, but exact values are build- and settings-specific |
| Polar Aim | Keep as explicit algorithm | Eight-point micro-motion | Clear implementation rather than a marketing label |
| Shake Aim | Keep for comparison | Alternating horizontal micro-motion | Often degrades precision; default Off |
| Velocity Aim | Add | Micro-motion scales with physical right-stick velocity | More adaptive than a fixed-radius pattern |
| Sticky / Batts Sticky | Consolidate | Compact four-point Sticky mode | These labels generally describe small right-stick patterns |
| Enhanced Rotational AA | Add cautiously | Left-stick pattern only when nearly stationary | Avoids fighting deliberate movement |
| AA V2 / V3 / V5 | Do not duplicate | Documented as non-standard vendor presets | Version labels do not describe interoperable algorithms |
| Enhanced Tracking | Rename | Aim micro-motion only | Controller-only code cannot observe a target |
| Aim Lock | Reject controller-only claim | None | True target lock needs visual target coordinates |
| Pro Aim | Do not use as a module name | Covered by explicit engines | Marketing name without a technical definition |
| Aim Abuse / ADS Spam | Remove | None | Disrupts ADS timing and is easy to conflict with normal play |
| Rumble weapon detection | Remove | None | Rumble varies with damage, effects, platform, and settings |
| Random “humanization” | Remove | None | Random output reduces repeatability and is not a compliance guarantee |
| GCV weapon detection | Add with calibration | 16-byte protocol, template classifier, confidence, hysteresis, stale timeout | Uses the player's exact capture feed and fails safe when data is missing |

## Context policy

Movement/action helpers run only when the master is enabled and Context Lock is off. Fast Loot additionally supports a safer activation chord and blocks while ADS or firing.

Controller input alone cannot identify:

- a Buy Station or loadout UI
- a reload prompt versus an interact prompt
- a teammate revive
- parachute deployment state
- the equipped weapon or optic

Those states are handled by the optional GCV classifier. The GPC2 script consumes only a 16-byte confidence-scored state packet and fails safe when frames are stale.

## Current Season 05 recoil facts

Official July 22, 2026 notes:

- FG42 MFS Ambilateral Stock: nearly all horizontal recoil removed, aggressive vertical recoil added.
- AN-94: about 8% base recoil reduction in BR/Resurgence.
- Voyak KT-3: 5% base recoil reduction in BR/Resurgence.
- Swordfish A1 MFS Penta Burst: recoil increased, particularly first-shot recoil.

These are relative changes, not absolute Titan stick values. Values should be measured per exact weapon build.

# WZ Lab Features

These entries re-add the older feature names without hiding their limits. All
related options default Off.

## Boosted Sprint Refresh

Menu path: **Sprint Input Mode -> Boosted Sprint Refresh**

This mode periodically re-sends the normal sprint/tactical-sprint input while
you are pushing fully forward and not ADS, firing, plating, using, or crouching.
It can help a setup enter tactical sprint quickly after a cancel or input miss.
It cannot exceed any movement-speed cap set by the game/server.

Primary setting:

| Setting | Default | Purpose |
|---|---:|---|
| Boosted Sprint Refresh Time | 900 ms | Spacing between refresh double taps |

## Quick Revive Hold Assist

Runtime chord: **D-Pad Up + Use/Reload**

This holds the normal interact/revive input for the configured duration. With
GCV Context Guard enabled, it only runs when the visual worker has a fresh
`REVIVE` UI match. With GCV disabled, it is a manual chord and should be tested
carefully because revive/interact/reload are shared inputs.

Primary settings:

| Setting | Default | Purpose |
|---|---:|---|
| Quick Revive Hold Assist | Off | Enables the helper |
| Quick Revive Hold Time | 4500 ms | Duration to hold Use/Reload |

## Rumble Profile Hint

This re-adds rumble-driven profile selection as a fallback. It samples the
strongest rumble motor while ADS + Fire and selects one recoil profile after the
rumble stays inside the calibrated window for the confirm time.

GCV weapon detection takes priority whenever it is fresh and confident. Rumble
can come from gunfire, damage, explosions, killstreaks, vehicles, controller
firmware, and platform effects, so treat it as a profile hint rather than true
weapon identification.

Primary settings:

| Setting | Default | Purpose |
|---|---:|---|
| Rumble Profile Hint | Off | Enables fallback selection |
| Rumble Low Threshold | 20 | Minimum accepted rumble value |
| Rumble High Threshold | 90 | Maximum accepted rumble value |
| Rumble Hint Profile | Profile 1 | Profile selected after confirmation |
| Rumble Confirm Time | 180 ms | Required stable rumble duration |

## Target / Aim-Lock Detection

This project keeps live CV output limited to HUD state: weapon, optic, UI
context, confidence, and profile. Player-target detection and aim-lock output
are not wired into the Titan packet or stick output path.

For private lab work, keep target experiments in a separate diagnostic script or
offline video test where the output is logs/overlays only. Do not send target
coordinates, aim angles, or stick corrections to `wz.gpc`. That separation lets
the WZ project keep fast, predictable controller timing and avoids mixing HUD
state helpers with a target-control system.

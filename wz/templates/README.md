# WZ CV Templates

The repository does not include copied game screenshots. Create templates from your own capture feed so they match your resolution, HUD scale, color settings, language, and capture card.

Use at least three clean images for each weapon or UI state:

```text
templates/
  weapons/
    fg42/
    an94/
    voyak_kt3/
    swordfish_a1/
  optics/
    iron/
    reflex/
    magnified/
  ui/
    buy_station/
    loadout/
    inventory/
    revive/
    parachute/
    reload/
```

The `tools/make_template.py` command reads the normalized ROI from `wz_cv_config.json`:

```powershell
py tools\make_template.py --image captures\fg42-01.png --group weapon --item FG42
py tools\make_template.py --image captures\buy-01.png --group ui --item BUY_STATION
```

Capture several lighting/background variations. Do not mix resolutions or change HUD scale after calibration. The GCV Context Guard remains fail-safe until every configured UI class has at least one template. The debug overlay reports the live confidence score; raise thresholds if a class false-matches and lower them slightly if correct templates consistently score just below threshold.

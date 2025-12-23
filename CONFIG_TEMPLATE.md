# Configuration Template - FPS Pro v9.1

Use this template to document your custom settings for different games.

---

## Game: _________________

**Date:** _________
**Script Version:** v9.1

---

### Anti-Recoil Settings

- **Enabled:** [ ] Yes  [ ] No
- **Activation Mode:** [ ] Hold  [ ] Toggle  [ ] Long Press  [ ] Conditional
- **Primary Key:** _______
- **Vertical Strength:** _____ (0-100)
- **Horizontal Adjust:** _____ (-20 to +20)
- **Notes:** _________________________________

---

### Movement Reset (Slide Cancel)

- **Enabled:** [ ] Yes  [ ] No
- **Activation Mode:** [ ] Hold  [ ] Toggle  [ ] Long Press  [ ] Conditional
- **Primary Key:** _______
- **Sprint Time:** _____ ms
- **Cancel Time:** _____ ms
- **Notes:** _________________________________

---

### Snaking (Prone Cycling)

- **Enabled:** [ ] Yes  [ ] No
- **Activation Mode:** [ ] Hold  [ ] Toggle  [ ] Long Press  [ ] Conditional
- **Primary Key:** _______
- **Cycle Time:** _____ ms
- **Notes:** _________________________________

---

### Wall Bounce (Jump Cancel)

- **Enabled:** [ ] Yes  [ ] No
- **Activation Mode:** [ ] Hold  [ ] Toggle  [ ] Long Press  [ ] Conditional
- **Primary Key:** _______
- **Jump Time:** _____ ms
- **Delay Time:** _____ ms
- **Notes:** _________________________________

---

### Drop Shot

- **Enabled:** [ ] Yes  [ ] No
- **Activation Mode:** [ ] Hold  [ ] Toggle  [ ] Long Press  [ ] Conditional
- **Primary Key:** _______
- **Secondary Key:** _______
- **Prone Time:** _____ ms
- **Notes:** _________________________________

---

### Bunny Hop

- **Enabled:** [ ] Yes  [ ] No
- **Activation Mode:** [ ] Hold  [ ] Toggle  [ ] Long Press  [ ] Conditional
- **Primary Key:** _______
- **Jump Duration:** _____ ms
- **Jump Interval:** _____ ms
- **Notes:** _________________________________

---

### Weapon Swap (YY)

- **Enabled:** [ ] Yes  [ ] No
- **Primary Key:** _______
- **Press Time:** _____ ms
- **Swap Interval:** _____ ms
- **Notes:** _________________________________

---

### Auto Sprint

- **Enabled:** [ ] Yes  [ ] No
- **Stick Threshold:** _____ (0-100)
- **Activation Delay:** _____ ms
- **Notes:** _________________________________

---

## Additional Notes

**What works well:**
- _________________________________
- _________________________________
- _________________________________

**What doesn't work:**
- _________________________________
- _________________________________

**Special combinations:**
- _________________________________
- _________________________________

**Performance issues:**
- _________________________________

---

## Quick Copy-Paste Values

```
Anti-Recoil: V=___ H=___ | Key=___
Slide Cancel: ST=___ CT=___ | Key=___
Snaking: Cycle=___ | Key=___
Wall Bounce: JT=___ DT=___ | Key=___
Drop Shot: PT=___ | Keys=___+___
Bunny Hop: JD=___ Int=___ | Key=___
Weapon Swap: PT=___ Int=___ | Key=___
Auto Sprint: Thresh=___ Delay=___
```

---

## Example: Call of Duty Warzone

**Date:** 2025-12-23
**Script Version:** v9.1

### Settings Used:

```
Anti-Recoil: V=30 H=3 | Key=RT | Mode=Hold
Slide Cancel: ST=80 CT=120 | Key=RB | Mode=Hold
Snaking: OFF
Wall Bounce: OFF
Drop Shot: OFF
Bunny Hop: OFF
Weapon Swap: PT=60 Int=120 | Key=Y | Mode=Hold
Auto Sprint: Thresh=60 Delay=100 | Always ON
```

**Notes:**
- Recoil at 30 works well for AR/SMG
- Slide cancel on RB for quick movement
- Weapon swap helps with animation cancels
- Bunny hop disabled (causes mantle issues)

---

**Save multiple copies of this template for different games!**

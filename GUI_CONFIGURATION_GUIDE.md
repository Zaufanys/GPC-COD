# GUI Configuration Guide - Gtuner IV

**Easy, No-Code Configuration for FPS Pro v9.2**

---

## 🎯 Overview

Version 9.2 introduces **full GUI configuration support**. You can now adjust all script parameters through the Gtuner IV interface without editing code!

---

## 🖥️ Accessing GUI Configuration

### Step 1: Open Gtuner IV
- Launch Gtuner IV application
- Connect your Cronus Zen device

### Step 2: Load the Script
1. Click **File** → **Open**
2. Navigate to `fps_pro_modular_v9.2.gpc`
3. Click **Open**

### Step 3: Open Device Configuration
1. Go to **Programmer** tab
2. Click **Device Configuration** button (or press F8)
3. Configuration panel opens on the right side

---

## 📋 Configuration Panel Layout

The Device Configuration panel shows all GUI-accessible variables:

```
┌─────────────────────────────────────────┐
│ Device Configuration                    │
├─────────────────────────────────────────┤
│                                         │
│ FEATURE TOGGLES                         │
│ ✓ _antirecoil_enabled      [✓]        │
│ ✓ _moverest_enabled        [ ]        │
│ ✓ _snaking_enabled         [ ]        │
│ ✓ _wallbounce_enabled      [ ]        │
│ ✓ _dropshot_enabled        [ ]        │
│ ✓ _bunnyhop_enabled        [ ]        │
│ ✓ _weapswap_enabled        [ ]        │
│ ✓ _autosprint_enabled      [✓]        │
│                                         │
│ RECOIL SETTINGS                         │
│ ✓ _antirecoil_vertical     [25]  ━━●   │
│ ✓ _antirecoil_horizontal   [5]   ━●━   │
│                                         │
│ TIMING PARAMETERS                       │
│ ✓ _movreset_sprint         [80]  ━━●   │
│ ✓ _movreset_cancel         [120] ━━━●  │
│ ✓ _snaking_cycle           [150] ━━━━● │
│ ... (more parameters)                   │
│                                         │
│ [Apply] [Reset] [Program Device]       │
└─────────────────────────────────────────┘
```

---

## 🎮 Configuration Variables Reference

### Feature Enable/Disable

| Variable | Default | Description |
|----------|---------|-------------|
| `_antirecoil_enabled` | ✅ TRUE | Enable/disable anti-recoil system |
| `_moverest_enabled` | ❌ FALSE | Enable/disable slide cancel |
| `_snaking_enabled` | ❌ FALSE | Enable/disable prone cycling |
| `_wallbounce_enabled` | ❌ FALSE | Enable/disable wall bounce |
| `_dropshot_enabled` | ❌ FALSE | Enable/disable drop shot |
| `_bunnyhop_enabled` | ❌ FALSE | Enable/disable bunny hop |
| `_weapswap_enabled` | ❌ FALSE | Enable/disable weapon swap |
| `_autosprint_enabled` | ✅ TRUE | Enable/disable auto sprint |

**How to Use:**
- **Checkboxes**: Click to toggle ON/OFF
- **Changes**: Take effect after programming device

---

### Recoil Settings

| Variable | Min | Max | Default | Description |
|----------|-----|-----|---------|-------------|
| `_antirecoil_vertical` | 0 | 100 | 25 | Vertical recoil compensation strength |
| `_antirecoil_horizontal` | -20 | +20 | 5 | Horizontal recoil compensation |

**How to Adjust:**

**Vertical (0-100):**
- `0` = No compensation
- `15-25` = Light recoil guns (SMGs, low-recoil ARs)
- `25-35` = Medium recoil (ARs, LMGs)
- `35-50` = High recoil (Heavy ARs, some LMGs)
- `50+` = Extreme recoil (special weapons)

**Horizontal (-20 to +20):**
- `0` = No horizontal adjustment
- `Positive (+5 to +20)` = Compensate for right drift
- `Negative (-5 to -20)` = Compensate for left drift

---

### Timing Parameters (All in Milliseconds)

#### Movement Reset (Slide Cancel)

| Variable | Range | Default | What It Controls |
|----------|-------|---------|------------------|
| `_movreset_sprint` | 50-150ms | 80ms | How long to hold sprint before cancel |
| `_movreset_cancel` | 80-200ms | 120ms | Delay after crouch cancel |

**Tuning Tips:**
- **Faster Cancel**: Decrease both values (70/100)
- **Slower Cancel**: Increase both values (100/140)
- **MW3/Warzone**: 80/120 (default works great)

---

#### Snaking (Prone Cycling)

| Variable | Range | Default | What It Controls |
|----------|-------|---------|------------------|
| `_snaking_cycle` | 100-200ms | 150ms | Time between stance changes |

**Tuning Tips:**
- **Fast Snaking**: 100-120ms (aggressive, may clip)
- **Medium Snaking**: 130-150ms (balanced)
- **Slow Snaking**: 160-200ms (smooth, safe)

---

#### Wall Bounce (Jump Cancel)

| Variable | Range | Default | What It Controls |
|----------|-------|---------|------------------|
| `_wallbounce_jump` | 50-150ms | 100ms | How long to hold jump |
| `_wallbounce_delay` | 100-200ms | 150ms | Delay between bounces |

**Tuning Tips:**
- **Quick Bounce**: 80/120ms
- **Standard**: 100/150ms (default)
- **Controlled**: 120/180ms

---

#### Drop Shot

| Variable | Range | Default | What It Controls |
|----------|-------|---------|------------------|
| `_dropshot_prone` | 50-150ms | 80ms | Speed of prone activation |

**Tuning Tips:**
- **Instant**: 50-70ms (very fast)
- **Standard**: 80-100ms (default)
- **Controlled**: 110-150ms (slower)

---

#### Bunny Hop

| Variable | Range | Default | What It Controls |
|----------|-------|---------|------------------|
| `_bunnyhop_jump` | 30-100ms | 50ms | Jump button press duration |
| `_bunnyhop_interval` | 50-200ms | 100ms | Time between jumps |

**Tuning Tips:**
- **Fast Hopping**: 40/70ms (rapid)
- **Standard**: 50/100ms (default)
- **Slow Hopping**: 70/150ms (controlled)
- **Fortnite**: 45/85ms (optimized)

---

#### Weapon Swap (YY)

| Variable | Range | Default | What It Controls |
|----------|-------|---------|------------------|
| `_weapswap_press` | 40-100ms | 60ms | Y button hold time |
| `_weapswap_interval` | 80-200ms | 120ms | Delay between first and second Y |

**Tuning Tips:**
- **Quick Swap**: 50/100ms
- **Standard**: 60/120ms (default)
- **Slow Swap**: 80/150ms

---

#### Auto Sprint

| Variable | Range | Default | What It Controls |
|----------|-------|---------|------------------|
| `_autosprint_threshold` | 30-90 | 60 | Stick push threshold to activate |

**Tuning Tips:**
- **Sensitive** (30-50): Activates easily, may trigger accidentally
- **Balanced** (55-70): Good for most users
- **Conservative** (75-90): Requires full stick push

---

## 🛠️ Configuration Workflows

### Workflow 1: Quick Setup (5 Minutes)

**For Call of Duty Players:**

1. Open Device Configuration (F8)
2. Enable features:
   - ✅ `_antirecoil_enabled`
   - ✅ `_moverest_enabled`
   - ✅ `_autosprint_enabled`
3. Adjust recoil:
   - `_antirecoil_vertical` → 30
4. Click **Program Device** (Ctrl+P)
5. Done!

---

### Workflow 2: Custom Game Setup

**For Other Games (Apex, Fortnite, etc.):**

1. **Identify Needed Features**
   - Apex: Anti-recoil, Wall Bounce, Weapon Swap
   - Fortnite: Anti-recoil, Bunny Hop, Auto Sprint

2. **Enable in GUI**
   - Check appropriate `_*_enabled` boxes

3. **Tune Recoil**
   - Test in-game, adjust `_antirecoil_vertical`
   - Start at 20, increase by 5 until comfortable

4. **Adjust Timings**
   - Default values work for most games
   - Fine-tune if needed

5. **Program and Test**
   - Ctrl+P to program
   - Test in practice mode
   - Iterate as needed

---

### Workflow 3: Advanced Optimization

**For Competitive Players:**

1. **Baseline Test**
   - Use default settings
   - Note what feels off

2. **Incremental Adjustments**
   - Change ONE parameter at a time
   - Test for 10+ minutes
   - Document results

3. **Find Sweet Spot**
   - Increase/decrease by 10ms intervals
   - Test until optimal

4. **Save Configuration**
   - Document final values in CONFIG_TEMPLATE.md
   - Keep backup of script

---

## 📝 Configuration Examples

### Example 1: Low Recoil Setup

**Use Case:** Playing with SMGs, low-recoil ARs

```
_antirecoil_enabled = TRUE
_antirecoil_vertical = 18
_antirecoil_horizontal = 2
```

---

### Example 2: Aggressive Movement Setup

**Use Case:** Run-and-gun playstyle

```
_moverest_enabled = TRUE
_movreset_sprint = 70
_movreset_cancel = 100
_bunnyhop_enabled = TRUE
_bunnyhop_interval = 80
_autosprint_enabled = TRUE
_autosprint_threshold = 50
```

---

### Example 3: Tactical Setup

**Use Case:** Slower, precise gameplay

```
_antirecoil_enabled = TRUE
_antirecoil_vertical = 35
_dropshot_enabled = TRUE
_dropshot_prone = 90
_weapswap_enabled = TRUE
_weapswap_press = 70
```

---

## 🔄 Applying Configuration Changes

### Method 1: Program Device (Recommended)

1. Make changes in Device Configuration panel
2. Click **Program Device** button (or Ctrl+P)
3. Wait for "Programming Complete" message
4. Changes are live immediately

**When to Use:**
- Making multiple changes
- Permanent configuration
- Starting fresh session

---

### Method 2: Live Reload (Advanced)

1. Make changes in GUI
2. Click **Apply** button
3. Click **Compile** (Ctrl+F7)
4. Click **Program Device** (Ctrl+P)

**When to Use:**
- Testing different values quickly
- Troubleshooting issues
- Development/debugging

---

## ⚠️ Important Notes

### Validation

**All values are automatically validated:**
- Too-high values → Clamped to maximum
- Too-low values → Clamped to minimum
- Invalid values → Reset to default

**Example:**
```
You set: _movreset_sprint = 300
Script sees: 150 (max allowed)
```

### Sync Timing

**GUI values sync to script:**
- **On Script Load**: Once at startup
- **On Program Device**: When you flash device

**Script values do NOT sync back to GUI:**
- In-game menu changes won't appear in GUI
- Persistent memory values won't show in GUI
- Use one configuration method at a time

### Compatibility

**GUI config works with:**
- ✅ Gtuner IV (Windows, macOS)
- ✅ Cronus Zen (all firmware)
- ✅ All supported games

**Does NOT work with:**
- ❌ Gtuner III (use v9.1 instead)
- ❌ Text editors (use in-game menu)

---

## 🎯 Best Practices

### 1. Start with Defaults
Always begin with default values, then adjust.

### 2. Change One Thing
Only modify one parameter at a time for testing.

### 3. Test in Practice Mode
Never test in ranked/competitive first!

### 4. Document Changes
Keep notes of what works in CONFIG_TEMPLATE.md.

### 5. Backup Your Script
Save a copy before major changes.

### 6. Use Realistic Values
Don't set everything to maximum - it won't work well.

---

## 🐛 Troubleshooting GUI Config

### Issue: Changes Don't Take Effect

**Solution:**
1. Verify you clicked **Program Device**
2. Check Cronus Zen is connected
3. Try **Compile** first, then **Program Device**
4. Restart Gtuner IV

---

### Issue: Can't See Configuration Panel

**Solution:**
1. Press **F8** to toggle panel
2. Go to **View** → **Device Configuration**
3. Ensure script is loaded first
4. Check Gtuner IV version (need 4.0+)

---

### Issue: Sliders Not Responding

**Solution:**
1. Click directly on slider handle
2. Use arrow keys for precise control
3. Type value in text box instead
4. Restart Gtuner IV

---

### Issue: Values Reset to Default

**Solution:**
1. Changes aren't saved in GUI - they're temporary
2. In-game menu changes override GUI
3. Persistent memory overrides GUI on next boot
4. Use **in-game menu** for permanent changes

---

## 🎓 Advanced Tips

### Tip 1: Profile Switching

Create multiple script files for different games:
```
fps_pro_v9.2_warzone.gpc
fps_pro_v9.2_apex.gpc
fps_pro_v9.2_fortnite.gpc
```

Load appropriate file before playing.

---

### Tip 2: Quick Testing Workflow

1. Set `_antirecoil_enabled = FALSE` in GUI
2. Program device
3. Test vanilla gameplay
4. Set `_antirecoil_enabled = TRUE`
5. Program device
6. Compare difference

---

### Tip 3: Export Configuration

Document your GUI settings:

```
// My MW3 Config - 2025-12-23
_antirecoil_enabled = TRUE
_antirecoil_vertical = 32
_antirecoil_horizontal = 4
_moverest_enabled = TRUE
_movreset_sprint = 85
_movreset_cancel = 125
_autosprint_enabled = TRUE
_autosprint_threshold = 65
```

Save as `.txt` file for reference.

---

## 📚 Related Documentation

- **README.md** - General usage guide
- **CHANGELOG_v9.2.md** - What's new in v9.2
- **TECHNICAL_DOCUMENTATION.md** - Advanced details
- **CONFIG_TEMPLATE.md** - Settings tracker

---

## ✅ Quick Reference

### Essential GUI Variables:

| Variable | Typical Value | Adjust For |
|----------|---------------|------------|
| `_antirecoil_vertical` | 20-35 | Gun type |
| `_movreset_sprint` | 70-90 | Movement speed |
| `_bunnyhop_interval` | 80-120 | Jump timing |
| `_autosprint_threshold` | 50-70 | Stick sensitivity |

---

## 🎮 Ready to Configure!

1. Open Gtuner IV
2. Load `fps_pro_modular_v9.2.gpc`
3. Press **F8** for Device Configuration
4. Adjust settings
5. Click **Program Device** (Ctrl+P)
6. Play!

**No code editing required - it's that easy!**

---

**Version:** v9.2
**Last Updated:** 2025-12-23
**Difficulty:** Beginner-Friendly ✅

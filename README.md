# FPS Pro Modular Script v9.1
### Advanced First-Person Shooter Enhancement for Cronus Zen

---

## 📋 Overview

This is a professional-grade GPC (Game Profile Code) script for Cronus Zen devices, designed for competitive first-person shooter games. It features 8 fully customizable controller mechanics with a real-time in-game configuration menu and persistent memory storage.

## ✨ Features

### Core Mechanics

1. **Anti-Recoil System**
   - Vertical and horizontal recoil compensation
   - Adjustable strength (0-100)
   - Intelligent rate adjustment
   - Works with all weapon types

2. **Movement Reset (Slide Cancel)**
   - Quick sprint-to-crouch animation cancel
   - Customizable timing
   - Perfect for fast-paced movement

3. **Prone Cycling (Snaking)**
   - Automated crouch/prone/stand cycling
   - Adjustable cycle speed
   - Ideal for evasive maneuvers

4. **Wall Bounce (Jump Cancel)**
   - Timed jump input sequences
   - Perfect for advanced movement tech
   - Customizable delay timing

5. **Drop Shot**
   - Instant prone while firing
   - Configurable activation
   - Can be combined with other mechanics

6. **Bunny Hop**
   - Automatic jump when moving
   - Movement-based activation
   - Adjustable jump intervals

7. **Rapid Weapon Swap**
   - Quick YY weapon swap
   - Animation canceling
   - Dual-tap support

8. **Auto Sprint**
   - Automatic sprint on forward movement
   - Adjustable stick threshold
   - Always-ready sprint mode

---

## 🎮 Quick Start

### Installation

1. Open **Cronus Zen Studio**
2. Create a new slot in the Programmer tab
3. Copy the contents of `fps_pro_modular_v9.gpc`
4. Paste into the code editor
5. Click **Compile** (Ctrl+F7)
6. Click **Program Device** (Ctrl+P)

### First Launch

On first run, the script will initialize with default settings:
- Anti-Recoil: **Enabled** (RT trigger)
- Auto Sprint: **Enabled** (automatic)
- All other features: **Disabled** (configure via menu)

### Opening the Menu

Press: **SELECT + DPAD_UP**

The LED will turn **yellow** when the menu is open.

---

## 📖 Menu Navigation

### Controls

| Button | Action |
|--------|--------|
| **DPAD_UP** | Move to previous option |
| **DPAD_DOWN** | Move to next option |
| **DPAD_LEFT** | Decrease value / Previous choice |
| **DPAD_RIGHT** | Increase value / Next choice |
| **SELECT** | Save and exit menu |

### Menu Structure

```
┌─────────────────────────────────────────┐
│  ANTI-RECOIL SETTINGS                   │
├─────────────────────────────────────────┤
│  [0] Anti-Recoil Enabled: ON/OFF       │
│  [1] Activation Mode: Hold/Toggle/...   │
│  [2] Primary Key: RT/LT/RB/...         │
│  [3] Vertical Strength: 0-100          │
│  [4] Horizontal Adjust: -20 to +20     │
├─────────────────────────────────────────┤
│  MOVEMENT RESET SETTINGS                │
├─────────────────────────────────────────┤
│  [5] Movement Reset Enabled: ON/OFF    │
│  [6] Activation Mode: Hold/Toggle/...   │
│  [7] Primary Key: RB/LB/X/...          │
├─────────────────────────────────────────┤
│  SNAKING SETTINGS                       │
├─────────────────────────────────────────┤
│  [8] Snaking Enabled: ON/OFF           │
│  [9] Activation Mode: Hold/Toggle/...   │
│  [10] Primary Key: LB/RB/...           │
├─────────────────────────────────────────┤
│  ... (continues for all features)       │
└─────────────────────────────────────────┘
```

---

## 🔧 Configuration Options

### Activation Modes

Each feature supports 4 activation modes:

1. **HOLD** - Active while key is held
   - Best for: Anti-Recoil, Drop Shot, Movement Reset

2. **TOGGLE** - Press once to enable, again to disable
   - Best for: Snaking, Auto Sprint

3. **LONG PRESS** - Hold key for 500ms to activate
   - Best for: Advanced users wanting precision

4. **CONDITIONAL** - Only active when ADS (aiming down sights)
   - Best for: Anti-Recoil when you only want it while aiming

### Key Assignment Options

Available keys for primary/secondary binding:
- RT (Right Trigger)
- LT (Left Trigger)
- RB (Right Bumper)
- LB (Left Bumper)
- A, B, X, Y (Face buttons)
- L3 (Left Stick Click)
- R3 (Right Stick Click)
- NONE (No secondary key required)

---

## 🎯 Default Keybindings

| Feature | Key | Mode | Status |
|---------|-----|------|--------|
| Anti-Recoil | RT | Hold | ✅ Enabled |
| Movement Reset | RB | Hold | ❌ Disabled |
| Snaking | LB | Toggle | ❌ Disabled |
| Wall Bounce | X | Hold | ❌ Disabled |
| Drop Shot | RT + B | Hold | ❌ Disabled |
| Bunny Hop | L3 | Hold | ❌ Disabled |
| Weapon Swap | Y | Hold | ❌ Disabled |
| Auto Sprint | Auto | Always | ✅ Enabled |

---

## 💡 LED Feedback System

The Cronus Zen LED provides real-time status:

| Color | Meaning |
|-------|---------|
| 🔵 **Blue** | Ready - No features active |
| 🔷 **Cyan** | 1 feature currently active |
| 🟢 **Green** | 2 features currently active |
| 🟠 **Blinking Orange** | 3+ features active |
| 🟡 **Yellow** | Configuration menu open |

---

## ⚙️ Advanced Customization

### Timing Adjustments

Edit these values in the script for fine-tuning:

```gpc
// Anti-Recoil
int recoil_vertical = 25;        // 0-100
int recoil_horizontal = 5;       // -20 to +20
int recoil_adjustment_rate = 18; // Speed of application

// Movement Reset
int movreset_sprint_time = 80;   // Sprint duration (ms)
int movreset_cancel_time = 120;  // Cancel delay (ms)

// Snaking
int snaking_cycle_time = 150;    // Time between stances (ms)

// Wall Bounce
int wallbounce_jump_time = 100;  // Jump hold time (ms)
int wallbounce_delay_time = 150; // Between jumps (ms)

// Drop Shot
int dropshot_prone_time = 80;    // Prone activation (ms)

// Bunny Hop
int bunnyhop_jump_time = 50;     // Jump duration (ms)
int bunnyhop_interval = 100;     // Between jumps (ms)

// Weapon Swap
int weapswap_press_time = 60;    // Y press duration (ms)
int weapswap_interval = 120;     // Between swaps (ms)

// Auto Sprint
int autosprint_threshold = 60;   // Stick threshold (0-100)
int autosprint_delay = 100;      // Activation delay (ms)
```

### Button Remapping

To change button assignments in code, edit the combo sections:

```gpc
combo MovementResetCombo {
    set_val(B_BUTTON, 100);  // Change B_BUTTON to your preferred key
    // ... rest of combo
}
```

---

## 🎲 Game-Specific Presets

### Call of Duty: Warzone / MW3

```
Anti-Recoil: ON (RT, Strength: 30)
Movement Reset: ON (RB, Hold)
Auto Sprint: ON (Threshold: 60)
Bunny Hop: OFF (causes issues with mantling)
```

### Apex Legends

```
Anti-Recoil: ON (RT, Strength: 20)
Wall Bounce: ON (X, Toggle)
Auto Sprint: ON
Weapon Swap: ON (Y, Hold)
```

### Fortnite

```
Anti-Recoil: ON (RT, Conditional, Strength: 25)
Bunny Hop: ON (L3, Hold, Interval: 80)
Auto Sprint: ON
Drop Shot: OFF (build mode conflict)
```

---

## 🔒 Feature Conflict Management

Some features shouldn't be used together:

| Feature A | Conflicts With | Reason |
|-----------|----------------|--------|
| Snaking | Drop Shot | Both use crouch/prone rapidly |
| Movement Reset | Bunny Hop | Timing conflicts |
| Wall Bounce | Bunny Hop | Both spam jump button |

**Tip:** The script will still work, but results may be unpredictable when conflicting features are active simultaneously.

---

## 🐛 Troubleshooting

### Script Won't Compile

1. Ensure you're using **Cronus Zen Studio** (not older software)
2. Check for any copy/paste formatting errors
3. Verify no extra characters were added

### Features Not Activating

1. Open menu (SELECT + DPAD_UP) and verify feature is **enabled**
2. Check that the correct **activation key** is assigned
3. Verify **activation mode** matches your usage pattern
4. Some features require movement (e.g., Bunny Hop)

### Recoil Compensation Too Strong/Weak

1. Open menu and adjust **Vertical Strength** (option 3)
2. Adjust **Horizontal Adjust** if gun pulls left/right (option 4)
3. Try different values: 15-20 (low), 25-35 (medium), 40+ (high)
4. Different weapons may need different settings

### Menu Not Opening

1. Verify you're pressing **SELECT + DPAD_UP** (not START)
2. Hold DPAD_UP for 300ms before releasing SELECT
3. Check that script is properly loaded and active

### Settings Not Saving

1. Always exit menu properly with SELECT (don't disconnect)
2. Settings save automatically on menu close
3. Check Cronus device memory isn't full

---

## 📊 Performance Notes

### Polling Rate

Script is optimized for **1000Hz polling** on PC:
- Uses `vm_timing = 0` for minimal delay
- No blocking loops or unnecessary waits
- Efficient combo execution

### Input Lag

Total system lag breakdown:
- **Cronus processing:** <1ms
- **USB polling:** 1ms (1000Hz)
- **Game input buffer:** 4-16ms (game dependent)

**Total:** ~5-17ms additional latency

---

## ⚖️ Fair Play Notice

This script provides controller enhancements that may be considered:
- ✅ **Allowed:** In private matches, customs, training modes
- ⚠️ **Gray Area:** In public matchmaking (varies by game)
- ❌ **Prohibited:** In competitive/ranked (most games)

**Use responsibly and check your game's Terms of Service.**

---

## 📝 Changelog

### v9.1 (Current)
- Full modular architecture
- Real-time configuration menu
- Persistent memory storage
- LED feedback system
- 8 core features
- 4 activation modes
- Conflict detection ready

---

## 🤝 Support & Contributions

For issues or improvements:
1. Check troubleshooting section above
2. Verify script version matches this README
3. Test with default settings first
4. Report bugs with specific reproduction steps

---

## 📜 License

This script is provided as-is for educational purposes.
Use at your own risk and in accordance with game ToS.

---

**Happy Gaming! 🎮**

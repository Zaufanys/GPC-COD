# Technical Documentation - FPS Pro v9.1

**For Advanced Users and Developers**

---

## 📐 Architecture Overview

### Code Structure

```
fps_pro_modular_v9.gpc
│
├── Section 1: Constant Definitions
│   ├── Button mappings (Xbox layout)
│   ├── Feature indices (0-7)
│   ├── Activation mode constants
│   └── Persistent memory slots
│
├── Section 2: Variable Declarations
│   ├── Feature control arrays
│   ├── Timing arrays
│   ├── Feature-specific parameters
│   └── Menu system variables
│
├── Section 3: Initialization
│   ├── Persistent memory check
│   ├── Settings load/default init
│   └── LED initialization
│
├── Section 4: Main Loop
│   ├── Menu activation check
│   ├── Process menu OR game features
│   └── LED feedback update
│
├── Section 5: Feature Processing
│   ├── Activation checking
│   └── Feature execution
│
├── Section 6: Feature Activation Logic
│   ├── Multi-mode activation system
│   └── Key press detection
│
├── Section 7: Feature Implementations
│   ├── Anti-Recoil
│   ├── Movement Reset
│   ├── Snaking
│   ├── Wall Bounce
│   ├── Drop Shot
│   ├── Bunny Hop
│   ├── Weapon Swap
│   └── Auto Sprint
│
├── Section 8: Combo Definitions
│   └── Button sequence macros
│
├── Section 9: Menu System
│   ├── Menu toggle
│   ├── Menu processing
│   └── Value adjustment
│
├── Section 10: Utility Functions
│   ├── Value cycling
│   ├── Clamping
│   └── Button helpers
│
├── Section 11: LED Feedback
│   └── Status indication logic
│
└── Section 12: Persistent Memory
    ├── Default initialization
    ├── Save all settings
    └── Load all settings
```

---

## 🔧 Core Systems

### 1. Feature Management System

**Indexed Arrays:**
```gpc
int feature_enabled[TOTAL_FEATURES];     // ON/OFF state
int activation_mode[TOTAL_FEATURES];     // How to activate
int key_primary[TOTAL_FEATURES];         // Main activation key
int key_secondary[TOTAL_FEATURES];       // Optional second key
int feature_active[TOTAL_FEATURES];      // Currently active?
int feature_toggle_state[TOTAL_FEATURES];// For toggle mode
int feature_timer[TOTAL_FEATURES];       // Timing control
int feature_delay[TOTAL_FEATURES];       // Custom delays
```

**Feature Index Mapping:**
```gpc
FEAT_ANTIRECOIL  = 0
FEAT_MOVEREST    = 1
FEAT_SNAKING     = 2
FEAT_WALLBOUNCE  = 3
FEAT_DROPMSHOT   = 4
FEAT_BUNNYHOP    = 5
FEAT_WEAPSWAP    = 6
FEAT_AUTOSPRINT  = 7
```

### 2. Activation Mode System

**Four Activation Modes:**

```gpc
MODE_HOLD (0):
- Active while key(s) pressed
- Immediate response
- Best for: Anti-Recoil, Drop Shot

MODE_TOGGLE (1):
- Press to enable, press again to disable
- Includes debounce (300ms)
- Best for: Snaking, persistent features

MODE_LONGPRESS (2):
- Requires 500ms hold to activate
- Prevents accidental activation
- Deactivates on release

MODE_CONDITIONAL (3):
- Requires primary + secondary keys + ADS
- Fine-grained control
- Best for: Situational features
```

**Implementation:**
```gpc
function check_feature_activation(int feat_idx) {
    int key1_pressed = is_key_pressed(key_primary[feat_idx]);
    int key2_pressed = TRUE;

    if(key_secondary[feat_idx] != KEY_NONE) {
        key2_pressed = is_key_pressed(key_secondary[feat_idx]);
    }

    if(activation_mode[feat_idx] == MODE_HOLD) {
        feature_active[feat_idx] = (key1_pressed && key2_pressed);
    }
    // ... other modes
}
```

### 3. Persistent Memory System

**Memory Map (80 slots available):**

```
Slot 0:       Initialization flag (42 = initialized)
Slots 1-8:    Feature enable states
Slots 9-16:   Activation modes
Slots 17-24:  Primary keys
Slots 25-32:  Secondary keys
Slots 33-40:  Timing delays
Slots 41-48:  Additional parameters
Slots 49-79:  Reserved for future use
```

**Save/Load Pattern:**
```gpc
// Saving
for(i = 0; i < TOTAL_FEATURES; i++) {
    pmem_write(PMEM_FEAT_START + i, feature_enabled[i]);
}

// Loading
for(i = 0; i < TOTAL_FEATURES; i++) {
    feature_enabled[i] = pmem_read(PMEM_FEAT_START + i);
}
```

### 4. Menu System

**State Machine:**
```
MENU_CLOSED (0) ─── SELECT+DPAD_UP ───> MENU_OPEN (1)
      ^                                       │
      │                                       │
      └──────────── SELECT ─────────────────┘
```

**Navigation Logic:**
```gpc
- menu_index: Current option (0-23)
- menu_nav_timer: Debounce (150ms)
- DPAD_UP/DOWN: Change option
- DPAD_LEFT/RIGHT: Adjust value
```

**Value Adjustment:**
```gpc
function adjust_menu_value(int direction) {
    // direction = -1 (left) or +1 (right)
    // Modifies appropriate variable based on menu_index
    // Uses cycle_value() for bounded options
    // Uses clamp_value() for numeric ranges
}
```

---

## 🎯 Feature Implementation Details

### Anti-Recoil

**Algorithm:**
```gpc
1. Read current stick position (STICK_RY)
2. Calculate compensation: recoil_vertical * rate / 100
3. Add to current position
4. Clamp result to -100/+100 range
5. Apply with set_val()
```

**Key Variables:**
- `recoil_vertical`: Upward compensation strength
- `recoil_horizontal`: Left/right adjustment
- `recoil_adjustment_rate`: Speed multiplier

**Tuning Guide:**
- Low recoil guns: 15-25
- Medium recoil: 25-35
- High recoil: 35-50
- Extreme recoil: 50+

### Movement Reset (Slide Cancel)

**State Machine:**
```
Step 0: Idle
  ↓ (activation)
Step 1: Sprint (L3 pressed for movreset_sprint_time)
  ↓ (timer expires)
Step 2: Crouch cancel (combo runs for movreset_cancel_time)
  ↓ (timer expires)
Step 0: Reset & deactivate
```

**Combo Sequence:**
```gpc
combo MovementResetCombo {
    set_val(B_BUTTON, 100);  // Crouch
    wait(60);
    set_val(B_BUTTON, 0);    // Release
    wait(60);
    set_val(B_BUTTON, 100);  // Re-press
    wait(60);
    set_val(B_BUTTON, 0);    // Final release
}
```

### Snaking

**Cycle Pattern:**
```
Crouch → Prone → Stand → Crouch → ...
  |       |        |
  50ms   100ms    50ms
```

**Implementation:**
```gpc
Step 0: Crouch (single tap)
Step 1: Prone (double tap)
Step 2: Stand (single tap)
→ Repeat every snaking_cycle_time (150ms default)
```

### Wall Bounce

**Jump Timing:**
```
Press A → Hold 100ms → Release → Wait 150ms → Deactivate
```

**Best Used:**
- Around corners
- During strafing
- Combined with directional movement

### Drop Shot

**Instant Prone:**
```gpc
1. Detect RT + B pressed
2. Execute double-tap B (prone)
3. Hold for dropshot_prone_time
4. Auto-deactivate
```

### Bunny Hop

**Conditional Activation:**
```gpc
if(abs(STICK_LY) > 30 OR abs(STICK_LX) > 30) {
    // Player is moving
    if(timer expired) {
        Jump for bunnyhop_jump_time
        Reset timer to bunnyhop_interval
    }
}
```

### Weapon Swap

**Double-Tap Pattern:**
```
Y pressed → Hold 60ms → Release → Wait 120ms →
Y pressed → Hold 60ms → Release → Deactivate
```

### Auto Sprint

**Threshold Detection:**
```gpc
if(STICK_LY < -autosprint_threshold) {
    // Forward movement detected
    if(delay timer expired) {
        Press L3
    }
}
```

---

## 🔌 Button Abstraction Layer

**Xbox → Generic Mapping:**

```gpc
// Physical → Logical
XB1_RT → RT
XB1_LT → LT
XB1_A  → A_BUTTON
XB1_B  → B_BUTTON
// ... etc

// Key Index → Physical Button
KEY_RT (0) → get_val(RT) > 50
KEY_LT (1) → get_val(LT) > 50
KEY_A  (4) → get_val(A_BUTTON)
// ... etc
```

**Why This Matters:**
- Easy to port to PlayStation layout
- Centralized button mapping
- Change one definition to remap globally

**PlayStation Conversion Example:**
```gpc
// Change this section for PS:
define A_BUTTON = PS4_CROSS;
define B_BUTTON = PS4_CIRCLE;
define X_BUTTON = PS4_SQUARE;
define Y_BUTTON = PS4_TRIANGLE;
// ... rest auto-updates
```

---

## ⚡ Performance Optimization

### 1. VM Timing

```gpc
int vm_timing = 0;
```
- **0** = No delay (fastest, for 1000Hz)
- **1** = Minimal delay (500Hz)
- **2** = Standard delay (250Hz)

### 2. Loop Optimization

**Avoid:**
```gpc
// BAD: O(n²) complexity
for(i = 0; i < 100; i++) {
    for(j = 0; j < 100; j++) {
        // processing
    }
}
```

**Use:**
```gpc
// GOOD: O(n) complexity
for(i = 0; i < TOTAL_FEATURES; i++) {
    // Single-level processing
}
```

### 3. Combo Execution

**Efficient Timing:**
```gpc
combo FastCombo {
    set_val(BUTTON, 100);
    wait(50);  // Minimum effective delay
    set_val(BUTTON, 0);
}
```

**Inefficient (Don't do this):**
```gpc
combo SlowCombo {
    wait(500);  // Blocking wait
    set_val(BUTTON, 100);
    wait(500);  // Another long wait
}
```

### 4. Conditional Short-Circuiting

```gpc
// Efficient: Checks enabled state first
if(feature_enabled[i] && complex_condition()) {
    // Only evaluates complex_condition if enabled
}

// Less efficient:
if(complex_condition() && feature_enabled[i]) {
    // Always evaluates complex_condition
}
```

---

## 🛠️ Adding New Features

### Step-by-Step Guide

**1. Update Constants:**
```gpc
define FEAT_MYFEATURE = 8;  // Next index
define TOTAL_FEATURES = 9;  // Increment total
```

**2. Add Variables:**
```gpc
int myfeature_param1 = 100;
int myfeature_param2 = 50;
int myfeature_step = 0;
```

**3. Create Implementation:**
```gpc
function execute_my_feature() {
    // Your logic here
    if(myfeature_step == 0) {
        // Step 1
        myfeature_step = 1;
        feature_timer[FEAT_MYFEATURE] = myfeature_param1;
    } else if(myfeature_step == 1) {
        // Step 2
        if(feature_timer[FEAT_MYFEATURE] <= 0) {
            myfeature_step = 0;
            feature_active[FEAT_MYFEATURE] = FALSE;
        }
    }
}
```

**4. Add to Main Loop:**
```gpc
function process_game_features() {
    // ... existing features
    if(feature_active[FEAT_MYFEATURE]) {
        execute_my_feature();
    }
}
```

**5. Add Menu Options:**
```gpc
// In adjust_menu_value():
else if(menu_index == 24) {  // Next index
    feature_enabled[FEAT_MYFEATURE] = !feature_enabled[FEAT_MYFEATURE];
}
// ... add more menu indices for parameters
```

**6. Update Persistent Memory:**
```gpc
// In save_all_settings():
pmem_write(PMEM_PARAM_START + 4, myfeature_param1);

// In load_all_settings():
myfeature_param1 = pmem_read(PMEM_PARAM_START + 4);

// In init_default_settings():
feature_enabled[FEAT_MYFEATURE] = FALSE;
key_primary[FEAT_MYFEATURE] = KEY_RB;
```

**7. Increment menu_max_index:**
```gpc
int menu_max_index = 25;  // Was 23, now 25 (added 2 options)
```

---

## 🧪 Testing & Debugging

### LED Debug Output

```gpc
// Signal debugging states with LED colors
led_set(LED_4, 100, 0, 0, -1);  // Red = Error state
led_set(LED_4, 0, 0, 100, -1);  // Green = Success
led_set(LED_4, 100, 100, 100, -1);  // White = Checkpoint reached
```

### Timing Validation

```gpc
// Add to init:
int debug_timer = 0;

// In main:
debug_timer += get_rtime();
if(debug_timer >= 1000) {  // Every 1 second
    // Do debug action (e.g., blink LED)
    debug_timer = 0;
}
```

### Feature State Monitoring

```gpc
// Add temporary code to check states:
if(get_val(START)) {  // Press START for status
    int count = 0;
    for(i = 0; i < TOTAL_FEATURES; i++) {
        if(feature_active[i]) count++;
    }
    // Blink LED 'count' times
    led_blink_count(count);
}
```

---

## 📊 Memory Usage

### RAM Usage Estimate

```
Constants: ~50 bytes
Variables: ~400 bytes
Arrays: ~200 bytes
Functions: ~2KB code
Combos: ~500 bytes code
────────────────────
Total: ~3.2KB / 32KB available (10% usage)
```

### Persistent Memory Usage

```
Used: 48 slots / 80 available (60%)
Reserved: 32 slots for expansion
Free: 0 slots immediate use
```

**Expansion Capacity:**
- Can add ~8 more features before memory pressure
- Alternative: Compress settings (bitfields)

---

## 🔐 Security Considerations

### Anti-Detection Notes

**This script is detectable by:**
1. Statistical analysis (perfect recoil patterns)
2. Timing analysis (inhuman precision)
3. Input monitoring (impossible input combinations)

**Mitigation Strategies:**
1. Add randomization to timing
2. Don't use multiple features simultaneously
3. Vary activation patterns
4. Use human-like delays

**Example Randomization:**
```gpc
// Instead of fixed timing:
wait(100);

// Use randomized timing:
wait(90 + (get_rtime() % 20));  // 90-110ms random
```

---

## 🎨 Customization Examples

### Example 1: Add Recoil Randomization

```gpc
// In execute_anti_recoil():
int random_offset = (get_rtime() % 5) - 2;  // -2 to +2
temp_val += (recoil_vertical + random_offset) * recoil_adjustment_rate / 100;
```

### Example 2: Add Haptic Feedback

```gpc
// When feature activates:
combo FeatureActivateFeedback {
    set_val(RUMBLE_A, 30);  // Light rumble
    wait(50);
    set_val(RUMBLE_A, 0);
}
```

### Example 3: Profile Switching

```gpc
// Add profile variable
int current_profile = 0;

// In menu, add profile switch:
if(menu_index == 99) {
    current_profile = cycle_value(current_profile, 0, 2, direction);
    load_profile(current_profile);
}

function load_profile(int profile) {
    if(profile == 0) {  // Aggressive
        recoil_vertical = 40;
        autosprint_threshold = 50;
    } else if(profile == 1) {  // Balanced
        recoil_vertical = 25;
        autosprint_threshold = 60;
    } else {  // Stealth
        recoil_vertical = 15;
        autosprint_threshold = 70;
    }
}
```

---

## 📖 GPC Language Reference

### Key Functions Used

```gpc
get_val(button)           // Read button value (-100 to 100)
set_val(button, value)    // Set button value
get_rtime()               // Get runtime since last iteration (ms)
get_ptime(button)         // Get press time for button (ms)
event_release(button)     // TRUE if button just released
check_active(btn, time)   // TRUE if held for time (ms)
combo_run(name)           // Execute combo sequence
wait(ms)                  // Wait in combo (blocking)
led_set(led, r, g, b, d)  // Set LED color (0-100 RGB, duration)
pmem_read(slot)           // Read persistent memory
pmem_write(slot, value)   // Write persistent memory
abs(value)                // Absolute value
```

### Data Types

```gpc
int      // Integer (-32768 to 32767)
int[]    // Integer array
define   // Compile-time constant
```

### Control Flow

```gpc
if(condition) { }
else if(condition) { }
else { }

for(i = 0; i < max; i++) { }
while(condition) { }

return value;
```

---

## 🐛 Common Pitfalls

### 1. Array Out of Bounds
```gpc
// BAD:
for(i = 0; i <= TOTAL_FEATURES; i++) {  // One too many!

// GOOD:
for(i = 0; i < TOTAL_FEATURES; i++) {
```

### 2. Integer Overflow
```gpc
// BAD:
int timer = 40000;  // Max is 32767!

// GOOD:
int timer = 0;
if(timer > 32000) timer = 0;  // Reset before overflow
```

### 3. Blocking Waits in Main
```gpc
// BAD (freezes script):
main {
    wait(1000);  // Don't use wait() in main!
}

// GOOD (use timers):
main {
    if(timer > 1000) {
        // Do action
        timer = 0;
    }
    timer += get_rtime();
}
```

### 4. Forgetting to Reset States
```gpc
// BAD:
function execute_feature() {
    feature_step++;  // Never resets!
}

// GOOD:
function execute_feature() {
    if(feature_step >= max_steps) {
        feature_step = 0;  // Reset
        feature_active[idx] = FALSE;
    }
}
```

---

## 📚 Additional Resources

### Official Documentation
- Cronus Zen User Guide: https://cronusmax.com/manual/
- GPC Language Reference: https://cronusmax.com/gpc/
- Device Library: https://cronusmax.com/device-library/

### Community Resources
- CronusMax Forums: https://cronusmax.com/forums/
- Discord Community: (various - check forums)
- GitHub Examples: (search "Cronus GPC")

---

## 🔄 Version History

### v9.1 (2025-12-23)
- Initial modular release
- 8 core features
- Real-time menu system
- Persistent storage
- LED feedback
- Multi-mode activation

### Future Roadmap
- v9.2: Add randomization options
- v9.3: Profile system
- v9.4: Game-specific auto-detection
- v10.0: AI-assisted recoil learning

---

**End of Technical Documentation**

For basic usage, see README.md
For quick reference, see QUICK_REFERENCE.md

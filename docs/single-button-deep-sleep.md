# Single-Button Power and Color Control with Deep Sleep (ESP32-C3)

> **Superseded** by [deep-sleep.md](deep-sleep.md) for the four-button disc. Kept for its detailed acceptance criteria and pitfalls.

## Goal

Battery-powered ESP32-C3 LED device controlled by one momentary button:

- **Press once while off:** turn on, showing the last used color.
- **Hold 3 seconds while on:** turn off and enter deep sleep.
- **Press 1, 2 or 3 times quickly while on:** select color 1, 2 or 3.

When off, the device is in deep sleep with LED power cut, drawing as little current as the board allows.

Before writing code, inspect the existing repo to determine the framework (ESP-IDF or Arduino-ESP32), the LED library, and the current pin assignments. Follow the existing conventions. The sleep APIs below are ESP-IDF functions, and they are also callable from Arduino-ESP32.

## Hardware Assumptions

Confirm each of these with me or from the repo before implementing. Put every pin and value in one config header.

| Item | Default | Notes |
|---|---|---|
| Button pin | GPIO3 | Must be GPIO0 to GPIO5. Only these can wake the C3 from deep sleep. Do not use GPIO9 (BOOT) or GPIO2 (strapping pin). |
| Button wiring | Active low, external 100k pull-up to 3.3 V | Do not rely on the internal pull-up during deep sleep. |
| LED power switch | P-channel MOSFET or load switch, enable pin configurable | Gate must have a hardware pull-up so LEDs stay **off** when the pin floats during sleep or boot. |
| LED data pin | From repo | Driven low before sleep so it does not back-power the strip. |
| Battery sense | ADC pin on GPIO0 to GPIO4 (ADC1), high-value divider (e.g. 2 x 1M with 100 nF to ground) | If the divider is small, it drains the battery in sleep. Flag this if present. |
| LED type and count | From repo | WS2812/SK6812 draw ~0.5 to 1 mA each even when showing black, which is why LED power must be cut. |

## Interaction Spec

| State | Input | Result |
|---|---|---|
| Sleeping | Button press (low level) | Wake, restore last color, turn LEDs on |
| On | 1 to 3 short presses, then 400 ms with no new press | Set color to tap count |
| On | 4 or more short presses | Clamp to color 3 (or ignore; make it a config option) |
| On | Hold 3000 ms | LEDs off immediately, wait for release, deep sleep |
| On | No input for `AUTO_OFF_MS` | Same shutdown path as a hold |
| On | Battery below cutoff | Brief low-battery indication, shutdown path |
| Waking | Battery below wake threshold | Brief low-battery indication (or none), back to sleep without lighting |

A press that becomes a long hold must **not** also count as a tap.

## Timing Constants

Put these in the config header:

```c
#define DEBOUNCE_MS          30
#define MULTI_TAP_WINDOW_MS  400   // wait after last release before acting
#define LONG_HOLD_MS         3000
#define RELEASE_SETTLE_MS    50    // after release, before sleeping
#define WAKE_HOLD_MS         0     // 0 = disabled; e.g. 500 to require a hold to turn on
#define AUTO_OFF_MS          (60UL * 60UL * 1000UL)  // 0 = disabled
#define BATT_WAKE_MIN_MV     3400  // refuse to turn on below this (resting)
#define BATT_CUTOFF_MV       3300  // shut down below this while on (filtered)
```

## Implementation Details

### Wake handling

1. At startup, read `esp_sleep_get_wakeup_cause()`.
2. If the cause is `ESP_SLEEP_WAKEUP_GPIO`, treat it as a power-on press.
3. On a cold boot (power applied, reset, flashing), go straight to sleep **unless** a debug/config flag says to start on. Do not light up just because the battery was connected.
4. If `WAKE_HOLD_MS > 0`, check that the button is still held for that long after boot. If not, go back to sleep. This prevents accidental wake in a bag. Note boot takes 100 to 300 ms, so measure from when code starts running.
5. Check battery voltage before enabling LED power.

### Entering deep sleep (single shutdown function used by every off path)

Order matters:

1. Send all-black to the LEDs.
2. Drive the LED data pin low.
3. Disable LED power (MOSFET off).
4. Save the current color (see State Persistence).
5. **Wait for the button to be released**, then wait `RELEASE_SETTLE_MS`. GPIO wakeup on the C3 is level-triggered. Sleeping while the button is held low causes an immediate wake.
6. Configure the wakeup:
   ```c
   esp_deep_sleep_enable_gpio_wakeup(1ULL << BUTTON_GPIO, ESP_GPIO_WAKEUP_GPIO_LOW);
   ```
7. If the LED power enable pin needs to hold a level during sleep, use `gpio_hold_en()` and `gpio_deep_sleep_hold_en()`. The hardware pull-up on the MOSFET gate is the primary safeguard; the hold is a backup.
8. `esp_deep_sleep_start()`.

### Button handling

- Non-blocking state machine polled from the main loop (or a GPIO interrupt plus a timestamp, then processing in the loop). No `delay()`-based detection.
- Debounce both edges.
- Track: press start time, whether the current press has passed `LONG_HOLD_MS`, tap count, last release time.
- When the hold reaches `LONG_HOLD_MS` while still pressed, trigger shutdown right away (LEDs go dark as feedback) and let the shutdown function wait for release.
- When `tap_count > 0` and `now - last_release > MULTI_TAP_WINDOW_MS`, apply the color and reset the count.
- Any button activity resets the auto-off timer.

### State persistence

- Use an `RTC_DATA_ATTR` variable for the color index so it survives deep sleep with no flash writes.
- Also write it to NVS, but only when it changes, so it survives battery removal. Validate on load and default to color 1 if missing or out of range.

### Battery monitoring

- Use the calibrated ADC API (`adc_cali` in ESP-IDF, `analogReadMilliVolts()` in Arduino), average several samples, and scale by the divider ratio.
- Read the resting voltage at wake before turning LEDs on.
- While on, LEDs cause voltage sag. Filter readings (e.g. moving average, require several consecutive low readings) so a brief white flash does not trigger shutdown.
- Low-battery indication: a short dim red blink is fine. Keep it short so it does not drain an already low cell.

### Boot time

- For ESP-IDF, enable `CONFIG_BOOTLOADER_SKIP_VALIDATE_IN_DEEP_SLEEP` and reduce bootloader log level to keep wake fast.
- Measure time from wake to LEDs on and report it.

## Development Pitfalls

- **Flashing a sleeping board:** the native USB serial/JTAG disappears during deep sleep. To flash, press the button to wake it, or hold BOOT while tapping reset. Consider a compile-time `DEBUG_STAY_AWAKE` flag.
- **Serial logs** are lost across deep sleep. Log the wakeup cause early after boot.
- **Floating pins in sleep:** anything that must stay in a defined state (LED power, LED data) needs a hardware pull resistor.
- **Board quiescent current:** if the board uses an AMS1117 regulator, has a power LED, or a USB-UART chip, sleep current will be in the mA range regardless of firmware. Flag this, don't try to fix it in code.

## Acceptance Criteria

- [ ] Cold boot (battery connected) does not light the LEDs and enters deep sleep.
- [ ] Single press from sleep turns on with the last color within ~300 ms.
- [ ] 1, 2 and 3 quick presses select colors 1, 2 and 3 reliably.
- [ ] A 3 s hold turns off and does **not** immediately wake again on release.
- [ ] A hold does not also register as a tap.
- [ ] Color survives sleep cycles and battery removal.
- [ ] Auto-off triggers after `AUTO_OFF_MS` with no input.
- [ ] Device refuses to turn on below `BATT_WAKE_MIN_MV` and shuts down below `BATT_CUTOFF_MV`.
- [ ] Measured sleep current, with a multimeter in series with the battery, is documented in the README. Target: under 100 µA with a low-quiescent regulator and LED power cut.

## Out of Scope (for now)

- Brightness control, animations, BLE or Wi-Fi.
- Power-latch circuit (MOSFET held by firmware) as an alternative to deep sleep.

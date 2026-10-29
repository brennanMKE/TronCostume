# ESP32-C3 + 18650 LED Power Build

Single 18650 cell powering an ESP32-C3 and a short 5V addressable LED strip (under 30 LEDs), with USB-C charging, charge status detection, and battery voltage monitoring.

## Parts

| Part | Notes |
|---|---|
| 18650 Li-ion cell + single-cell holder | 3.7V nominal, 4.2V full. Not LiFePO4. |
| TP4056 USB-C charger module with protection (DW01 + 8205A) | Pads: B+/B- (battery), OUT+/OUT- (load), +/- (alt 5V input) |
| MT3608 boost module (HW-045) | Set to 5.0V before connecting anything |
| SPST switch | Between TP4056 OUT+ and MT3608 VIN+ |
| ESP32-C3 board | Powered from the 5V rail |
| WS2812B / SK6812 strip, under 30 LEDs | 5V |
| 470 to 1000 uF electrolytic capacitor | Across strip 5V/GND |
| 330 ohm resistor | Series on LED data line, at the strip end |
| 2x Schottky diode (1N5819, BAT54, or similar) | Charge status inputs |
| 2x 100k resistor + 0.1 uF capacitor | Battery voltage divider |
| 10k + 20k resistor (optional) | USB power detect divider |

## Power Path

```
18650 --> TP4056 B+/B-
          TP4056 OUT+ --> switch --> MT3608 VIN+
          TP4056 OUT- ------------> MT3608 VIN-
                                    MT3608 VOUT+ --> 5V rail (strip 5V, ESP32-C3 5V pin)
                                    MT3608 VOUT- --> GND rail
```

All grounds are common.

## MT3608 Setup (do this first)

1. Connect only the battery side (through the switch). Nothing on VOUT.
2. Meter on VOUT+/VOUT-.
3. Turn the blue trimpot until it reads 5.0V. It is multi-turn (about 25 to 30 turns), so go slowly.
4. Lock the trimpot with a dab of nail polish or hot glue.
5. After connecting the strip, run the brightest capped scene and confirm VOUT stays at about 4.8V or higher and the module is warm at most.

The switch must be on the input side. A boost converter passes input voltage through to the output when idle, so cutting only the output does not fully turn things off.

## Current Budget

- Practical MT3608 output from one cell: about 1A at 5V.
- ESP32-C3 with WiFi: about 100mA.
- Strip budget: cap at **800mA** in FastLED.
- Each WS2812 draws about 60mA at full white, so 30 LEDs at full white (1.8A) is over budget. The cap handles this automatically.
- The TP4056 protection trips around 3A from the cell, well above what this setup pulls.

## ESP32-C3 Pin Map

| GPIO | Use | Notes |
|---|---|---|
| 3 | Battery voltage (ADC1) | Via 100k/100k divider |
| 6 | TP4056 CHRG status | Via Schottky diode, INPUT_PULLUP |
| 7 | TP4056 STDBY status | Via Schottky diode, INPUT_PULLUP |
| 4 | USB power detect (optional) | Via 10k/20k divider from TP4056 input 5V |
| 10 | LED data | Through 330 ohm resistor |

Avoid GPIO2, GPIO8, GPIO9 (strapping pins) and GPIO5 (ADC2, unreliable on C3).

## Charge Status Wiring

The TP4056 status pins are open-drain and pull low when active. Their LEDs are pulled up to 5V, so never connect them directly to a C3 GPIO (3.3V only).

- **CHRG** = TP4056 pin 7 (red LED cathode side)
- **STDBY** = TP4056 pin 6 (green LED cathode side)

For each one:

```
TP4056 status pin --|<|-- ESP32-C3 GPIO (INPUT_PULLUP)
             (diode cathode toward TP4056)
```

| CHRG | STDBY | State |
|---|---|---|
| LOW | HIGH | Charging |
| HIGH | LOW | Full |
| HIGH | HIGH | No USB power, or no battery |

The LED cathode pads are easier to solder to than the IC pins.

## Battery Voltage Wiring

```
Cell + (TP4056 B+) --[100k]--+--[100k]-- GND
                             |
                             +-- GPIO3
                             |
                           [0.1uF]
                             |
                            GND
```

- 4.2V cell gives 2.1V at the pin, inside the C3's ~0 to 2.5V ADC range.
- Divider draws about 20uA continuously, negligible for an 18650.

## USB Detect Wiring (optional)

```
TP4056 input + --[10k]--+--[20k]-- GND
                        |
                        +-- GPIO4
```

5V in gives about 3.3V at the pin. Separates "unplugged" from "no battery" in the both-HIGH status case.

## Code

```cpp
#include <FastLED.h>

#define LED_PIN     10
#define NUM_LEDS    30
#define VBAT_PIN    3
#define CHRG_PIN    6
#define STDBY_PIN   7
#define USB_PIN     4

#define LED_MAX_MA  800
#define LOW_BATT_V  3.40f
#define CRIT_BATT_V 3.20f

CRGB leds[NUM_LEDS];

enum ChargeState { NOT_CHARGING, CHARGING, FULL };

float readBatteryVolts() {
  uint32_t total = 0;
  for (int i = 0; i < 16; i++) {
    total += analogReadMilliVolts(VBAT_PIN);
    delay(2);
  }
  return (total / 16.0f) * 2.0f / 1000.0f;  // x2 undoes the divider
}

int batteryPercent(float v) {
  // Rough Li-ion resting voltage curve
  const float volts[] = {3.30, 3.50, 3.65, 3.75, 3.85, 3.95, 4.10, 4.20};
  const int   pct[]   = {   0,   10,   25,   40,   55,   70,   90,  100};
  if (v <= volts[0]) return 0;
  if (v >= volts[7]) return 100;
  for (int i = 1; i < 8; i++) {
    if (v < volts[i]) {
      float t = (v - volts[i - 1]) / (volts[i] - volts[i - 1]);
      return pct[i - 1] + t * (pct[i] - pct[i - 1]);
    }
  }
  return 100;
}

ChargeState readChargeState() {
  bool chrg  = digitalRead(CHRG_PIN)  == LOW;
  bool stdby = digitalRead(STDBY_PIN) == LOW;
  if (chrg && !stdby) return CHARGING;
  if (stdby && !chrg) return FULL;
  return NOT_CHARGING;
}

// Debounce: TP4056 status can flicker with no battery or at state changes
ChargeState stableChargeState() {
  static ChargeState last = NOT_CHARGING;
  static ChargeState candidate = NOT_CHARGING;
  static uint32_t since = 0;
  ChargeState now = readChargeState();
  if (now != candidate) {
    candidate = now;
    since = millis();
  } else if (now != last && millis() - since > 1500) {
    last = now;
  }
  return last;
}

bool usbPresent() {
  return digitalRead(USB_PIN) == HIGH;
}

void setup() {
  Serial.begin(115200);
  pinMode(CHRG_PIN, INPUT_PULLUP);
  pinMode(STDBY_PIN, INPUT_PULLUP);
  pinMode(USB_PIN, INPUT);

  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setMaxPowerInVoltsAndMilliamps(5, LED_MAX_MA);
}

void loop() {
  static uint32_t lastReport = 0;

  float v = readBatteryVolts();
  ChargeState cs = stableChargeState();

  // Low battery handling
  if (v < CRIT_BATT_V && !usbPresent()) {
    FastLED.clear(true);
    esp_deep_sleep_start();  // wake requires reset or power cycle
  } else if (v < LOW_BATT_V) {
    FastLED.setBrightness(40);
  } else {
    FastLED.setBrightness(255);
  }

  // Your animation here
  fill_rainbow(leds, NUM_LEDS, millis() / 20, 8);
  FastLED.show();

  if (millis() - lastReport > 5000) {
    lastReport = millis();
    const char* s = cs == CHARGING ? "charging" : cs == FULL ? "full" : "not charging";
    Serial.printf("Battery %.2fV (%d%%), %s, USB %s\n",
                  v, batteryPercent(v), s, usbPresent() ? "yes" : "no");
  }

  delay(20);
}
```

## Calibration

1. Measure the cell with a multimeter.
2. Compare to the serial output.
3. If consistently off, multiply the result in `readBatteryVolts()` by a correction factor (meter reading / reported reading). Resistor tolerance alone can shift it 1 to 2%.

## Notes and Gotchas

- **Voltage readings shift with load and charging.** Voltage sags under LED load and reads high while charging. Percentage is most accurate at rest. Use voltage, not percentage, for decisions.
- **Charging with the load on** works, but the TP4056 may never terminate (red LED stays on) because the load keeps current flowing. Turn the switch off for a clean charge.
- **USB-C chargers:** many TP4056 boards lack the CC resistors USB-C PD chargers require, so some chargers supply nothing. Use a simple charger or a USB-A to C cable.
- **TP4056 protection** cuts off around 2.4 to 2.5V. The firmware cutoff at 3.2V is gentler on the cell.
- **Data level:** 3.3V data into WS2812 at 5V usually works. If the first LED flickers, add a 74AHCT125 level shifter.
- **Single cell only.** The TP4056 cannot charge cells in series.

# Deep Sleep and Power Switching

**Status: after Halloween.** For Halloween, "off" (hold a button 3 s) only darkens the LEDs, and the power switch is the real off. This doc is the plan for a proper low-power off, and the hardware it needs.

It replaces the one-button design in [single-button-deep-sleep.md](single-button-deep-sleep.md) for the four-button disc. That doc's shutdown order and pitfalls still apply and are summarized below.

## What Deep Sleep Does

The ESP32-C3's processor, radio and almost all memory switch off, and the LEDs go dark. A tiny always-on part of the chip watches one pin. Pressing that button restarts the board in about 0.3 s, and it comes back in the color it was showing.

- **It can't hear ESP-NOW.** A sleeping cloak won't receive anything from the disc, so the cloak gets its own wake button (see [The cloak](#the-cloak)).
- **The USB connection disappears.** To flash a sleeping board, press its wake button first, or hold BOOT and tap reset.
- **The wake press only wakes.** It isn't counted as a tap, and it doesn't light anything by itself. The costume lights once the disc and cloak have found each other (see [Waking up together](#waking-up-together)).
- **Power-on works the same as waking.** Switching the disc on, or plugging in the cloak's battery pack, starts that board the same way as a wake press. Nothing goes back to sleep on its own at power-up.

## Where the Battery Goes

The chip itself draws a few microamps in deep sleep. Everything else on the battery is what decides standby time. These numbers are estimates; measure with a multimeter in series with the battery.

| Setup while "off" | Draw | 2500 mAh 18650 lasts |
|---|---|---|
| Awake, LEDs dark (Halloween build) | ~100 mA | ~1 day |
| Deep sleep, strip still powered | ~20-35 mA | ~3-5 days |
| Deep sleep + MOSFET cutting strip power | ~2-5 mA | ~3-6 weeks |
| Also remove the board's power LED, low-drain boost converter | under 0.5 mA | months |
| Power switch off | 0 | the battery's own shelf life |

What still draws power in deep sleep:

- **The LED strip**: each WS2812 draws about 0.5-1 mA even when dark, so 30 LEDs is 15-30 mA. The MOSFET below removes this.
- **The MT3608 boost converter**: keeps running with nothing to power, a few mA.
- **The Super Mini's red power LED**: about 1-3 mA, always on unless removed.

## Wake Buttons

Only GPIO 0-5 can wake the C3, so each board's wake button is on **GPIO 5** (`WAKE_PIN`):

| Board | Wake button | Other buttons |
|---|---|---|
| Disc | Black (GPIO 5) | White, blue, green (GPIO 6, 7, 10) can't wake it |
| Cloak | Its one button (GPIO 5 to GND) | None |

While asleep, GPIO 5 has to stay HIGH until pressed. Try the chip's internal pull-up held through sleep first. If the board wakes by itself, or won't wake, add a **100 kΩ resistor from GPIO 5 to 3.3V**.

Wake is level-triggered: if the board goes to sleep while black is still held, it wakes straight away. Shutdown waits for every button to be released first.

## Waking Up Together

The disc owns the color and saves it in flash (NVS). The cloak never picks a color itself:

1. **Disc wakes** (black button, or power switch): it **lights straight away in its saved color**. The black press that woke it is ignored until released, so it doesn't also toggle the outer ring. **Built.**
2. **Cloak wakes** (its button, or power reconnected): it stays dark until the disc tells it what to show. Today that's the disc's next heartbeat (within 1 s). **Built.** Planned: it broadcasts `HELLO` every `CLOAK_HELLO_MS` (200 ms) and the disc answers at once.
3. **If the cloak hears nothing** for `CLOAK_LINK_WAIT_MS` (5 min), it goes back to deep sleep rather than sit awake and dark. Planned.

The cloak only ever shows a color the disc sent, so the two can't disagree. A cloak joining late lights in whatever the disc is already showing.

## Cutting Strip Power with a MOSFET

### What a MOSFET is

A MOSFET is a switch controlled by a voltage instead of a finger. It has three pins:

| Pin | Job | Switch analogy |
|---|---|---|
| **Gate (G)** | The control input | The finger pressing the switch |
| **Source (S)** | One side of the switch | Contact 1 |
| **Drain (D)** | The other side | Contact 2 |

The voltage on the gate, measured relative to the source, opens or closes the path between drain and source. Almost no current flows into the gate, so a GPIO can control a strip drawing amps.

- **N-channel** turns on when the gate is *higher* than the source. It goes on the **ground** side of a load.
- **P-channel** turns on when the gate is *lower* than the source. It goes on the **5V** side of a load.

### Why a P-channel on the 5V side

Cutting the strip's **ground** with an N-channel looks simpler, but addressable LEDs then find another path to ground through the **data wire** into the ESP32. The strip stays partly powered, and it can back-power the ESP32 through the data pin.

Cutting the **5V** side avoids that. So the standard approach is a **P-channel MOSFET between the 5V rail and the strip's 5V**.

### Why it needs a helper transistor

To turn a P-channel *off*, its gate must go all the way up to its source voltage, here 5V. A GPIO only reaches 3.3V, leaving the gate 1.7V below the source, which is enough to keep many P-channels partly on. A small N-channel transistor in between does the switching for the GPIO.

### The circuit

```
 5V rail ──────────┬──── S ┌─────────┐ D ──── strip 5V
 (boost out)       │       │ P-FET   │
                [100k]     └────┬────┘
                   │            G
                   └────────────┤
                                │
                                D ┌─────────┐
                                  │ 2N7000  │  (small N-channel driver)
                                  └────┬────┘
                                  S    G
                                  │    │
                                 GND   ├──[220Ω]── GPIO 20 (LED_POWER_PIN)
                                       │
                                     [100k]
                                       │
                                      GND
```

| GPIO 20 | 2N7000 | P-FET gate | Strip |
|---|---|---|---|
| **HIGH** (awake, lights on) | On, pulls the P-FET gate to GND | 0V, 5V below the source | **Powered** |
| **LOW**, or floating in sleep | Off | Pulled up to 5V | **No power** |

Each resistor's job:

- **100k, P-FET gate to 5V**: keeps the strip **off by default**, in deep sleep, at power-up and while flashing, with no help from the firmware.
- **100k, 2N7000 gate to GND**: keeps the driver off while GPIO 20 is floating.
- **220Ω, GPIO to 2N7000 gate**: limits the current spike when the GPIO switches.

GPIO 20 is free (serial runs over USB) and stays quiet at boot. A cold boot keeps the strip dark, which also stops the brief flash of random colors these strips sometimes show at power-up.

### Parts

| Part | What to look for |
|---|---|
| P-channel MOSFET | On-resistance (R<sub>DS(on)</sub>) rated at **V<sub>GS</sub> = −4.5V or lower**, at least 2A. The **AO3401** is a common choice, but it's surface-mount (SOT-23) and needs a small adapter board. Avoid parts rated only at −10V (such as the IRF9540); they won't fully turn on from 5V. |
| Driver | **2N7000** (TO-92, often in starter kits). A **2N3904** NPN with a 1 kΩ base resistor also works. |
| Resistors | 2 × 100 kΩ, 1 × 220 Ω |

**Pin order differs between parts.** Check the datasheet's pinout drawing before soldering. A P-FET fitted backwards conducts through its internal diode and never switches off.

### Load switch IC: the one-chip alternative

A **load switch** IC packages the P-FET, the driver and the default-off behavior into one chip with an enable pin that takes 3.3V logic directly. Look for one rated for **5V input, 2A or more, and an active-high enable**. It replaces the five parts above with one part plus an input capacitor. Most come in small surface-mount packages, so they need an adapter board or a ready-made breakout module. If one is available as a breakout, it's the easiest route.

### Leaving room for it now

On the protoboard, reserve space for the two transistors and three resistors (or a load switch breakout), and three connections:

- **5V in** from the boost converter
- **5V out** to the strip
- **GPIO 20** from the ESP32

Until it's fitted, run a wire straight from 5V in to 5V out. Removing that wire is the only rewiring needed later.

## Power Switch on the Button Board

A physical power switch is still the only true zero-drain off. The power build ([esp32c3-18650-led-power.md](esp32c3-18650-led-power.md)) puts it between the TP4056 output and the MT3608 input. That's the battery side, so it must stay on the input side of the boost converter.

It can sit on the protoboard with the four buttons, so everything you touch is in one place:

- **Rating**: on the battery side, 5V at 1A out of the boost converter is about **1.5-1.8A** at 3.3-3.7V in. A **2A** switch is just enough; **3A** gives margin. Slide or small toggle switches with these ratings are common.
- **Wiring**: the battery current runs out to the protoboard and back, so use two short wires of **22 AWG or heavier** to the switch. Don't route it through thin jumper wire.
- **Cloak**: no switch needed. It runs from a USB battery pack, and unplugging the pack is its off switch (see [The cloak](#the-cloak)).

The power switch and the MOSFET do different jobs. The switch is for storage and travel. The MOSFET makes deep sleep worth using between wears.

## The Cloak

**Power**: the cloak runs from a USB battery pack. The pack's 5V feeds the Super Mini's 5V pin and the strip directly, so the cloak has no 18650, TP4056 or MT3608. For long storage, unplug the pack.

**Button**: one momentary button from GPIO 5 to GND, the wake pin. It can sit anywhere on the cloak that's easy to reach.

| Cloak button | Result |
|---|---|
| Press while asleep | Wakes, stays dark, looks for the disc ([Waking up together](#waking-up-together)) |
| Press while awake | Nothing |
| Hold 3 s while awake | Asks the disc to turn the costume off. The disc schedules off for both, so they go dark together |

The cloak button never changes the lights directly. It always goes through the disc, so the two can't disagree.

**Sleeping**: the cloak goes to deep sleep when the disc tells it to (`SLEEP`), or after `CLOAK_LINK_WAIT_MS` with no disc. It stays asleep until its button is pressed or power is reconnected. There's no timed wake-and-listen.

**Battery packs that switch themselves off**: many USB packs cut power when the draw drops below about 50-100 mA. A sleeping cloak draws a few mA, so the pack will probably shut off within a minute. That's fine: the cloak loses power completely, and pressing the pack's button or replugging it starts the cloak again as a power-on. On those packs the pack becomes the off switch, and the cloak button is a backup for packs that stay on.

**Strip power**: with no boost converter, the main standby drain is the strip. The MOSFET still helps if the pack stays on while the cloak sleeps.

## Messages to Add

| Message | Direction | Purpose |
|---|---|---|
| `HELLO` | cloak → disc, every 200 ms while awake and unlinked | "I'm awake and dark, tell me what to show" |
| `SLEEP` | disc → cloak (and partner's cloak for tap-then-hold) | Go to deep sleep now |
| `OFF_REQUEST` | cloak → disc | Cloak button held 3 s: please turn the costume off |

All carry `COSTUME_ID` like the existing messages. `SLEEP` is sent several times, like `SET_COLOR`, since broadcasts aren't acknowledged.

## Shutdown Order (every off path)

1. Show all-black on the strip.
2. Drive the LED data pin (GPIO 4) LOW, so it can't back-power the strip.
3. Set GPIO 20 LOW: strip power off (once the MOSFET is fitted).
4. Make sure the current color is saved (it normally already is, `COLOR_SAVE_MS` after the last change).
5. Wait for every button to be released, then about 50 ms more.
6. Enable GPIO wake on GPIO 5, LOW level.
7. `esp_deep_sleep_start()`.

On wake (or power-on): read `esp_sleep_get_wakeup_cause()` for the log, set GPIO 20 HIGH, and follow [Waking up together](#waking-up-together).

The disc restores its color from flash (NVS) on both wake and power-on, so there's one path. Off is never saved, so it always comes back lit. The cloak never stores a color; it always gets one from the disc.

## Firmware Steps

`WAKE_PIN`, the cloak's `BUTTON_PINS`, `LED_POWER_PIN` and the link timings (`CLOAK_HELLO_MS`, `CLOAK_LINK_WAIT_MS`) are already in `include/config.h`.

1. Drive `LED_POWER_PIN` HIGH at boot. It does nothing until the MOSFET is fitted, so it's safe to add now.
2. **Waking up together**: add `HELLO` so the disc answers a waking cloak at once instead of on the next heartbeat. (Disc restore and dark cloak start are built.)
3. **Disc sleep**: replace "hold to off" with the shutdown sequence, sending `SLEEP` to the cloak first.
4. **Cloak sleep**: sleep on `SLEEP`, or after `CLOAK_LINK_WAIT_MS` unlinked; wake on GPIO 5; hold 3 s sends `OFF_REQUEST`.
5. ~~Save the disc's color to NVS~~ Built (`COLOR_SAVE_MS`).
6. Measure standby current with a multimeter in series with the battery and record it here.

Step 2 is useful even before deep sleep: it also speeds up a cold power-on.

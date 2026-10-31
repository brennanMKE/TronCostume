# Tron Identity Disc

Tron cloak and Identity Disc lights for two costumes, worn as a couple. In each costume the cloak and the disc each have an ESP32-C3 driving its own addressable LED strip, and the boards talk over **ESP-NOW**. Buttons on the disc set the color, and the cloak changes at the same moment.

Each disc has four buttons: **black, white, blue, green**. Six colors come in pairs: white/yellow, blue/red, green/orange.

- **Tap** white, blue or green: your disc and cloak change to that color.
- **Double tap**: the paired color (yellow, red, orange).
- **Hold 1 s**, or **tap then hold 1 s** (both costumes planned): the same, for both costumes at once.
- **Black**: tap turns the outer ring on or off (or ends an effect), a double tap gives an erratic flicker, a triple tap gives motion. Hold 3 s turns your costume off.

See [docs/controls.md](docs/controls.md) for the full controls.

![Single-gap C-shaped light window](Single-gap%20C-shaped%20light%20window.png)

## Features

- **Disc controls the cloak**: Three color buttons on the disc, each with a primary and a secondary color. The cloak follows the disc.
- **Outer ring effects**: The inner C is always a solid color; the outer ring can be off, steady, flickering or circling, set with the black button.
- **Hold to turn off**: Hold black for 3 s and your disc and cloak go dark together. Tap any button to come back on.
- **Change together or separately** (both planned): A tap changes your own costume; the same gesture held for 1 s changes both costumes at once. See [docs/controls.md](docs/controls.md).
- **Simultaneous change**: The disc schedules each change 50 ms ahead and tells the cloak exactly how long is left, corrected for measured radio latency, so both strips switch together.
- **Two costumes, no crosstalk**: Each costume has its own `COSTUME_ID`, so a single tap on costume 1's disc only controls costume 1's cloak, even side by side.
- **Self-healing sync**: The disc sends a heartbeat every second carrying its color. If a press is lost in the air, or the cloak reboots, the cloak catches up.
- **One code base**: All four boards build from the same source, keyed on `COSTUME_ID` and `DEVICE_ROLE`. No WiFi network, router or MAC addresses to configure.
- **Battery powered** (planned): The disc runs from a single 18650 cell with USB-C charging; the cloak from a USB battery pack. See [docs/esp32c3-18650-led-power.md](docs/esp32c3-18650-led-power.md).
- **Deep sleep** (after Halloween): "Off" today only darkens the LEDs; the boards stay awake. A real low-power mode is planned. See [docs/deep-sleep.md](docs/deep-sleep.md).

## Hardware Platform

Each board (cloak and disc):

- **Microcontroller**: ESP32-C3
- **LEDs**: WS2812B (addressable), on GPIO 4 through a 330 ohm resistor. GPIO 4 sits next to 3.3V, 5V and GND on the C3 Super Mini.
- **Power**: disc: 18650 + TP4056 charger + MT3608 boost to 5V. Cloak: a USB battery pack straight to 5V.

Disc only, four momentary buttons on a protoboard. Each one goes from its GPIO to GND; no resistors needed (the firmware enables the internal pull-ups).

| Button | GPIO |
|---|---|
| Black | 5 |
| White | 6 |
| Green | 7 |
| Blue | 10 |

All four are lined up on one side of the Super Mini in that order, skipping GPIO 8 (onboard LED, strapping pin) and 9 (BOOT, strapping pin). GPIO 0 and 1 are free for later additions.

Black is on GPIO 5 on purpose: only GPIO 0-5 can wake the C3 from deep sleep, so black doubles as the wake button for the future low-power mode, with no extra wiring.

The disc's LED chain is the inner C (`MAIN_LEDS`) followed by the outer ring (`RING_LEDS`). See [docs/disc-build.md](docs/disc-build.md).

Pins, LED limits and timing live in [include/config.h](include/config.h).

## Costumes and Roles

Each build environment sets two constants:

| Env | `COSTUME_ID` | `DEVICE_ROLE` |
|---|---|---|
| `disc-1` | 1 | `ROLE_DISC` |
| `cloak-1` | 1 | `ROLE_CLOAK` |
| `disc-2` | 2 | `ROLE_DISC` |
| `cloak-2` | 2 | `ROLE_CLOAK` |

- **`COSTUME_ID`** pairs a disc with its cloak. Every packet carries it, and boards drop packets from any other costume. For a third costume, add `disc-3` / `cloak-3` envs.
- **`DEVICE_ROLE`** decides behavior. The disc reads the button, owns the color and measures latency; the cloak follows. A board also drops packets from its own role, which catches two boards flashed as the same thing (it logs `Ignoring packet from role ...`).

Anything that has to differ between disc and cloak, such as LED count, goes in the `#if DEVICE_ROLE` block at the top of [include/config.h](include/config.h).

Label each board with its env name once flashed. Nothing on the board itself says which costume it belongs to.

## How ESP-NOW Works Here

ESP-NOW is Espressif's connectionless radio protocol. Boards send small packets (up to 250 bytes) straight to each other using the WiFi radio, with no access point and no IP.

1. Every board puts the radio in station mode, stays off any WiFi network, locks to `ESPNOW_CHANNEL` (default 1) and turns modem power save off (power save adds tens of ms of receive delay).
2. Every packet goes to the broadcast address `FF:FF:FF:FF:FF:FF`, so no board needs another's MAC.
3. Each packet carries a magic number (`"DISC"`), the sender's `COSTUME_ID` and role. Anything that isn't from the other half of this costume is dropped.

| Message | Direction | Purpose |
|---|---|---|
| `PING` | disc → cloak, every 1 s | Heartbeat with the disc's target color; starts a latency measurement |
| `PONG` | cloak → disc | Echoes the `PING` so the disc can time the round trip |
| `SET_COLOR` | disc → cloak, on press | Scheduled color change |
| `SET_COLOR_GROUP` (planned) | disc → all four boards, on double tap | Scheduled color change for both costumes |

### Changing color at the same time (latency handling)

No library covers this for Arduino. Espressif's ESP-NOW time sync module is ESP-IDF only and needs their full ESP-NOW stack. So the firmware does a small version itself, without syncing clocks:

1. **Measure latency.** Each `PING` carries the disc's send time. The cloak echoes it in a `PONG`, along with how long it held the packet before replying. The disc subtracts the hold time to get the radio round trip and keeps **half of the smallest round trip over the last 8 pings** as the one-way latency. The minimum is the sample least delayed by retries.
2. **Schedule, don't fire.** A press schedules the disc's own change `APPLY_DELAY_MS` (50 ms) ahead and sends `SET_COLOR` with the **time remaining** and the latency estimate.
3. **Cloak lines up.** The cloak timestamps the packet the moment it arrives and schedules its change at `arrival + remaining - latency`, which is the same instant as the disc.
4. **Survive loss.** Broadcasts aren't acknowledged, so `SET_COLOR` goes out 3 times, 12 ms apart, inside the 50 ms window. Each copy carries its own remaining time. The cloak acts on the first copy that arrives.

Only a short interval (under 50 ms) crosses the air, so crystal drift between the boards (tens of parts per million, well under a microsecond here) doesn't matter. The remaining error is any difference between send and receive latency, which should be well under a millisecond and far below what a person can see. `APPLY_DELAY_MS` can go anywhere up to 250 ms; 50 ms already reads as instant.

Full details, a worked example and the tunables are in [docs/latency-handling.md](docs/latency-handling.md).

Measure the real offset by setting `SYNC_DEBUG_PIN` in `config.h` to a free GPIO on both boards. It toggles on every color change; put a scope or logic analyzer on both pins.

### How you know they're connected

- `Peer Cloak found` / `Peer Disc found` on first contact.
- `Peer LOST` after about 3.5 s of silence (`PEER_TIMEOUT_MS`), then `Peer back` when it returns.
- A `[stats]` line every 5 s with received count, lost packets (from sequence gaps), link state `up` / `LOST` / `none`, and on the disc the current latency estimate.

This is serial-only for now. It is the hook for a visible indicator later, such as a short blink on the disc when the cloak drops out.

## Testing with Two Boards

Before the protoboard is built, a jumper wire from GPIO 5, 6, 7 or 10 to GND acts as a button. An LED strip on GPIO 4 is optional. [../ButtonsAndColors](../ButtonsAndColors) is a breadboard practice project with the same pins.

1. Plug in both boards and find their ports:
   ```bash
   pio device list
   ```
2. Flash one as costume 1's disc and the other as its cloak:
   ```bash
   pio run -e disc-1  -t upload --upload-port /dev/cu.usbmodemXXXX
   pio run -e cloak-1 -t upload --upload-port /dev/cu.usbmodemYYYY
   ```
3. Open a monitor on each, in two terminals:
   ```bash
   pio device monitor --port /dev/cu.usbmodemXXXX
   pio device monitor --port /dev/cu.usbmodemYYYY
   ```

The disc should print something like:

```
TronIdentityDisc costume 1 Disc
My MAC: 7C:DF:A1:12:34:56  channel 1
Peer Cloak found: 7C:DF:A1:AB:CD:EF
[stats] color=blue rx=5 lost=0 txFail=0 peer=up latency=900us
```

| Test | Expected |
|---|---|
| Tap blue on the disc | After about 0.4 s, disc logs `Color -> blue (button)`, cloak logs `Color -> blue (disc button)`, strips change together |
| Double tap blue | Both change to red |
| Hold green 1 s | Disc logs `Both costumes -> green (group message not built yet ...)` and both change to green |
| Tap black | Disc logs `Outer ring off`; the ring part of the disc strip goes dark, the C stays lit |
| Double tap black, then triple tap black | `Outer ring on (flicker)`, then `(motion)` |
| Hold black 3 s | Disc logs `Hold: lights off`, both log `Color -> off` |
| Tap black while off | Both come back on in the saved color |
| Power-cycle the cloak | Cloak comes up dark, then lights in the disc's color within a second (`disc sync`) |
| Pick red, wait 2 s (`Saved red`), power-cycle the disc | Disc logs `Restored red` and lights red at once |
| Power on the disc while holding black | Comes back in the saved color; the ring isn't toggled |
| Unplug the cloak | Disc logs `Peer LOST` within about 3.5 s |
| Plug the cloak back in | Cloak logs `Color -> ... (disc sync)` from the next heartbeat |
| Move the boards apart | `lost` climbs and `latency` rises as range runs out |
| Flash a board as `disc-2` / `cloak-2` | Costume 1 and costume 2 ignore each other |
| Flash both as `disc-1` | Each logs `Ignoring packet from role 0` and they do not sync |

## Build Instructions

This project uses [PlatformIO](https://platformio.org/).

```bash
# Build all four
pio run -e disc-1 -e cloak-1 -e disc-2 -e cloak-2

# Upload (always name the env)
pio run -e disc-1  -t upload
pio run -e cloak-1 -t upload

# Monitor serial output
pio device monitor
```

`default_envs` is `disc-1` only, so a bare `pio run -t upload` flashes one image rather than every image to the same port in turn.

FastLED is pinned to 3.10.3. Newer releases fail to compile against the Arduino 2.x core that `espressif32` 6.x ships.

## Project Layout

```
include/config.h          Costume/role, pins, LED limits, ESP-NOW and sync timing
include/every_n_millis.h  Rollover-safe timer helpers
src/main.cpp              ESP-NOW link, latency measurement, scheduled color change, button, LEDs
docs/                     Hardware and design notes
```

## Open Items

- **Change both costumes**: the 1 s hold gestures are built but only change your own costume until `GROUP_ID` and `SET_COLOR_GROUP` are added. See [docs/controls.md](docs/controls.md).
- **Dock sensor**: a Hall sensor on GPIO 3 so the outer ring stays off while the disc is on your back. See [docs/disc-build.md](docs/disc-build.md).
- **Verify sync on hardware**: measure the real offset with `SYNC_DEBUG_PIN` (a free pin such as GPIO 0) on a scope, or with a 240 fps phone video of both strips. Record the result in [docs/latency-handling.md](docs/latency-handling.md); add a fixed correction only if the offset is consistent and visible.
- **Power doc pin map is out of date**: [docs/esp32c3-18650-led-power.md](docs/esp32c3-18650-led-power.md) has LED data on GPIO 10, charge status on 6/7 and USB detect on 4. With LED data now on 4, buttons on 5/6/7/10 and the dock sensor on 3: battery sense could use GPIO 0 or 1 (ADC1). Charge status would need GPIO 20/21, but 20 is reserved for the MOSFET, so probably skip it (the TP4056's own LEDs show charging). None of this is needed for the prototype.
- **Low-power off** (after Halloween): planned in [docs/deep-sleep.md](docs/deep-sleep.md). Black (GPIO 5) wakes the disc; the cloak gets one wake button on GPIO 5 and runs from a USB battery pack. The disc saves its color to flash and lights in it at power-on or wake; the cloak stays dark until the disc tells it what to show. A P-channel MOSFET on GPIO 20 can cut strip power; reserve protoboard space for it now. A 2-3A power switch can go on the disc's button protoboard, which now has room for it.
- Battery monitoring and low-battery cutoff from the power doc.

## Docs

- [docs/frame.md](docs/frame.md): The plywood frame: three bays, access covers and their insert blocks, and the front and back insert positions. The reference for every other part.
- [docs/front-face.md](docs/front-face.md): Step 1 of the build: the front face (3 mm black, white C inlay, 10 mm white outer ring), light separation, frame layout and face screw positions.
- [docs/disc-build.md](docs/disc-build.md): Disc build plan: black face with inlaid white C, 9 mm white outer ring, laminated plywood frame, two sideways LED channels, three inner-rim bays, magnetic back dock, and a render brief for an exploded view.
- [docs/controls.md](docs/controls.md): Single tap, double tap and hold: what each changes, messages, implementation plan.
- [docs/latency-handling.md](docs/latency-handling.md): Latency handling, how disc and cloak change color at the same moment: latency measurement, scheduling, loss handling, accuracy, verification.
- [docs/esp32c3-18650-led-power.md](docs/esp32c3-18650-led-power.md): 18650 power build, pin map, current budget.
- [docs/deep-sleep.md](docs/deep-sleep.md): Deep sleep plan, battery budget, MOSFET strip power switch, power switch on the button board, cloak wake.
- [docs/single-button-deep-sleep.md](docs/single-button-deep-sleep.md): Earlier one-button deep sleep spec, superseded by deep-sleep.md.

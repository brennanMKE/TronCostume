# Tron Identity Disc

Tron cloak and Identity Disc lights for two costumes. In each costume the cloak and the disc each have an ESP32-C3 driving its own addressable LED strip, and the two boards talk over **ESP-NOW**. Buttons on the disc set the color, and the cloak changes at the same moment.

The disc has four buttons: **white, blue, red, green**. Hold any one for 3 seconds to turn off both the disc and the cloak; press any button to turn them back on in that color.

![Single-gap C-shaped light window](Single-gap%20C-shaped%20light%20window.png)

## Features

- **Disc controls the cloak**: One button per color on the disc. The cloak has no buttons and follows the disc.
- **Hold to turn off**: Hold any button for 3 s and both strips go dark together. Press any button to come back on.
- **Simultaneous change**: The disc schedules each change 50 ms ahead and tells the cloak exactly how long is left, corrected for measured radio latency, so both strips switch together.
- **Two costumes, no crosstalk**: Each costume has its own `COSTUME_ID`, so costume 1's disc only controls costume 1's cloak, even side by side.
- **Self-healing sync**: The disc sends a heartbeat every second carrying its color. If a press is lost in the air, or the cloak reboots, the cloak catches up.
- **One code base**: All four boards build from the same source, keyed on `COSTUME_ID` and `DEVICE_ROLE`. No WiFi network, router or MAC addresses to configure.
- **Battery powered** (planned): A single 18650 cell with USB-C charging on each board. See [docs/esp32c3-18650-led-power.md](docs/esp32c3-18650-led-power.md).
- **Deep sleep** (after Halloween): "Off" today only darkens the LEDs; the boards stay awake. A real low-power mode is planned. See [docs/single-button-deep-sleep.md](docs/single-button-deep-sleep.md).

## Hardware Platform

Each board (cloak and disc):

- **Microcontroller**: ESP32-C3
- **LEDs**: WS2812B (addressable), under 30 LEDs, on GPIO 10 through a 330 ohm resistor.
- **Power**: 18650 + TP4056 charger + MT3608 boost to 5V.

Disc only, four momentary buttons on a protoboard. Each one goes from its GPIO to GND; no resistors needed (the firmware enables the internal pull-ups).

| Button | GPIO |
|---|---|
| White | 0 |
| Blue | 1 |
| Red | 3 |
| Green | 4 |

These are all on GPIO 0-5 on purpose: only those pins can wake the C3 from deep sleep, so any button can become a wake button later without rewiring. Avoid GPIO 2, 8 and 9 (strapping pins, they affect boot) and GPIO 10 (LED data).

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

Before the protoboard is built, a jumper wire from GPIO 0, 1, 3 or 4 to GND acts as a button. An LED strip on GPIO 10 is optional.

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
| Press the red button on the disc | Disc logs `Color -> red (button)`, cloak logs `Color -> red (disc button)`, strips change together |
| Hold any button 3 s | Disc logs `Hold: lights off`, both log `Color -> off` |
| Press any button while off | Both come back on in that button's color |
| Power-cycle the cloak while off | Cloak comes up, then goes dark within a second (`disc sync`) |
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

- **Verify sync on hardware**: measure the real offset with `SYNC_DEBUG_PIN` (GPIO 5) on a scope, or with a 240 fps phone video of both strips. Record the result in [docs/latency-handling.md](docs/latency-handling.md); add a fixed correction only if the offset is consistent and visible.
- **GPIO 3 conflict**: the power doc puts battery voltage sense on GPIO 3, and the white/blue/red/green buttons take GPIO 0, 1, 3 and 4. Battery sense isn't needed for the prototype; it needs a new pin before it's added.
- **Low-power off** (after Halloween): "off" only blanks the LEDs. The ESP32-C3 with its radio kept awake (about 80-100 mA) plus the idle WS2812s (about 1 mA each) still draw roughly 100+ mA. That's maybe 20 hours on a 2500 mAh 18650, so use the power switch for real storage. A sleeping board also can't receive ESP-NOW, so the cloak will need its own way to wake. [docs/single-button-deep-sleep.md](docs/single-button-deep-sleep.md) was written for one button and three colors and needs updating for the four-button layout.
- Battery monitoring and low-battery cutoff from the power doc.

## Docs

- [docs/latency-handling.md](docs/latency-handling.md): Latency handling, how disc and cloak change color at the same moment: latency measurement, scheduling, loss handling, accuracy, verification.
- [docs/esp32c3-18650-led-power.md](docs/esp32c3-18650-led-power.md): 18650 power build, pin map, current budget.
- [docs/single-button-deep-sleep.md](docs/single-button-deep-sleep.md): Single-button on/off and color control with deep sleep.

# Latency Handling: Changing Disc and Cloak Color at the Same Moment

How the disc and its cloak change color together, despite radio latency, without synchronizing their clocks. The implementation is in [src/main.cpp](../src/main.cpp); the tunables are in [include/config.h](../include/config.h).

## The Idea

The disc never says "change now". It says "change in X ms", and changes itself at the same moment.

A radio message always takes time to arrive, so a cloak that reacts on arrival is always behind. Instead, the disc schedules its own change `APPLY_DELAY_MS` (50 ms) after the press. That gives the message time to arrive and the cloak time to line up. Delays under about 100 ms between pressing a button and seeing the light read as instant, so 50 ms is invisible.

The two clocks never need to agree. Only a relative interval ("this much time is left") crosses the air.

## Messages

| Message | Direction | Fields used |
|---|---|---|
| `PING` | disc → cloak, every `HEARTBEAT_MS` (1 s) | `stampUs` = disc send time, `color` = disc target color |
| `PONG` | cloak → disc, reply to each `PING` | `stampUs` = echoed, `aUs` = cloak hold time |
| `SET_COLOR` | disc → cloak, on press or hold | `color`, `event`, `aUs` = time remaining, `latencyUs` |

All timestamps are `esp_timer_get_time()` microseconds (64-bit, no rollover).

## Step 1: Measure Latency (continuously)

```
disc clock                                   cloak
  t1 ── PING (t1) ──────────────────────────▶ arrives
                                              holds it h µs
  t4 ◀───────────────────────── PONG (t1, h)
```

- Round trip = `t4 − t1 − h`. Both `t1` and `t4` come from the disc's clock, so no clock sync is needed.
- One-way latency ≈ half the round trip.
- The disc keeps the **minimum round trip over the last `LATENCY_WINDOW` (8) pings**. Retries and busy air only ever make a trip slower, never faster, so the fastest recent sample is the most accurate.
- Until the first `PONG` arrives, `LATENCY_DEFAULT_US` (1500 µs) is used.
- Samples outside 0-100 ms are discarded.

The disc prints the estimate in its `[stats]` line as `latency=…us`.

## Step 2: The Press

When a button is pressed at disc time T:

1. The disc schedules its own change at `T + APPLY_DELAY_MS`.
2. It sends `SET_COLOR` with the color, an event id, the **time remaining** until that moment, and its **latency estimate**.

## Step 3: The Cloak Lines Up

The cloak timestamps the packet in the ESP-NOW receive callback, before it is queued, then schedules its change at:

```
arrival + remaining − latency
```

Worked example:

| | Disc clock (µs) | Cloak clock (µs) |
|---|---|---|
| Disc sends `SET_COLOR`, 49,800 µs left | 1,000,200 | |
| Packet arrives, 900 µs later | | 5,000,900 |
| Cloak schedules 5,000,900 + 49,800 − 900 | | **5,049,800** |
| Disc applies | **1,050,000** | |

Both apply 49,800 µs after the send, even though the clocks read completely different numbers.

## Step 4: Surviving Loss

Broadcast ESP-NOW has no acknowledgment, so a packet can vanish silently.

- **Repeats**: `SET_COLOR` is sent `SET_COLOR_REPEATS` (3) times, `SET_COLOR_REPEAT_MS` (12 ms) apart, all inside the 50 ms window. Each copy recomputes its own time remaining, so any copy gives the right moment. The cloak acts on the first copy and ignores repeats with the same event id. `config.h` refuses to compile if the repeats don't fit inside the window.
- **Heartbeat fallback**: every `PING` carries the disc's target color. If all copies are lost, or the cloak reboots, the cloak catches up within a second. It's late in that case, but never stuck out of sync.
- **No undo by a stale heartbeat**: the disc's `PING` carries the *pending* color during the 50 ms window, and the cloak ignores heartbeat colors while it has a change scheduled. A ping sent just before a press can't revert it.
- **Off**: holding a button for 3 s sends `COLOR_OFF` through exactly the same path.

Two costumes don't interfere: every packet carries `COSTUME_ID`, and boards drop packets from other costumes.

## Expected Accuracy

Remaining sources of error, largest first:

| Source | Size (estimated) | Notes |
|---|---|---|
| Send vs receive asymmetry | tens to a few hundred µs | Round-trip/2 assumes both directions take the same time |
| Receive timestamp placement | small, fairly steady | Stamped in the WiFi-task callback, slightly after the radio receives |
| Loop polling | µs | Each board checks for a waiting change on every pass through `loop()`; nothing in it blocks |
| Crystal drift | < 1 µs | Only a 50 ms interval crosses the air |
| `FastLED.show()` | ~1 ms, cancels | Both boards take the same time to push 30 LEDs |

Expected total: well under 1 ms, versus 16.7 ms for one 60 fps camera frame. This is an estimate from the design and **has not been measured on hardware yet**.

Modem power save is turned off (`esp_wifi_set_ps(WIFI_PS_NONE)`), because it adds tens of ms of receive delay. The cost is higher idle current.

## Verifying on Hardware

1. **Slow-motion video**: film both strips side by side at 240 fps (about 4 ms per frame). They should change in the same frame.
2. **Scope or logic analyzer**: set `SYNC_DEBUG_PIN` to `5` in `include/config.h` on both boards. The pin toggles right after each strip updates, so the gap between the two traces is the real error.

If the offset is consistent (for example, the cloak always 300 µs late), add a fixed correction to the cloak's schedule. That's probably unnecessary.

## Tunables

| Constant | Default | Effect |
|---|---|---|
| `APPLY_DELAY_MS` | 50 | Press-to-light delay on both boards. Up to ~250 ms is fine; must cover latency plus all repeats |
| `SET_COLOR_REPEATS` | 3 | Copies of each change sent |
| `SET_COLOR_REPEAT_MS` | 12 | Spacing between copies |
| `HEARTBEAT_MS` | 1000 | `PING` period: latency sample rate and catch-up time |
| `LATENCY_WINDOW` | 8 | Pings kept for the minimum round trip |
| `LATENCY_DEFAULT_US` | 1500 | Latency used before the first `PONG` |
| `PEER_TIMEOUT_MS` | 3500 | Silence before `Peer LOST` is logged |
| `SYNC_DEBUG_PIN` | -1 | GPIO toggled on each apply, for measuring; -1 = off |

## Why Not a Library

No Arduino library does ESP-NOW time sync. Espressif's [ESP-NOW time synchronization module](https://docs.espressif.com/projects/esp-now/en/latest/esp32/api-reference/time/espnow_time.html) is ESP-IDF only and needs their full ESP-NOW stack and framing. The Arduino core's [ESP-NOW API](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/espnow.html) has no sync protocol. The scheme here is about 60 lines and needs no clock sync, because only a relative interval crosses the air.

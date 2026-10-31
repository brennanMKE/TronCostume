# Controls: Four Buttons

**Status:**
- **Built** in `src/main.cpp`: the gestures, the colors, own-costume changes, the outer ring on/off and its effects.
- **Not yet built:** changing **both costumes** with `SET_COLOR_GROUP`. Until it is, a "both" gesture changes your own costume only and logs that.

## Who Wears What

| Costume | Boards |
|---|---|
| 1 | `disc-1` + `cloak-1` |
| 2 | `disc-2` + `cloak-2` |

All four boards are one **group**. A disc and its cloak always show the same color.

## Buttons

Lined up on one side of the ESP32-C3 Super Mini, in this order:

| Button | GPIO | Job |
|---|---|---|
| Black | 5 | Outer ring, off, and wake from deep sleep |
| White | 6 | White / yellow |
| Green | 7 | Green / orange |
| Blue | 10 | Blue / red |

LED data is on GPIO 4. GPIO 8 (onboard LED) and 9 (BOOT) are skipped. Black is on GPIO 5 because only GPIO 0-5 can wake the C3. GPIO 0 and 1 are free for additions later.

## Colors

Each color button has a **primary** and a **secondary** color:

| Button | Primary (tap) | Secondary (double tap) |
|---|---|---|
| White | White `#E6FFFF` | Yellow `#FFE64D` |
| Blue | Blue `#6FC3DF` | Red `#FF2A2A` |
| Green | Green `#39FF14` | Orange `#DF740C` |

## The Controls

### White, blue, green

| Gesture | Your disc + cloak | Partner's disc + cloak |
|---|---|---|
| **Tap** | Primary color | Unchanged |
| **Double tap** | Secondary color | Unchanged |
| **Hold 1 s** | Primary color | Primary color, at the same moment |
| **Tap, then hold 1 s** | Secondary color | Secondary color, at the same moment |

### Black

| Gesture | Result |
|---|---|
| **Tap** | Back to steady: the outer ring on and solid. Never turns anything off |
| **Double tap** | Outer ring: erratic flicker |
| **Triple tap** | Outer ring: motion (a bright section circling) |
| **Hold 3 s** | Your disc and cloak off, then the disc deep sleeps ([deep-sleep.md](deep-sleep.md)) |
| **Press while asleep** | Wakes the disc in the saved color, with the cloak lighting at the same moment. White, blue and green do nothing while it sleeps |
| **Tap while off** | With `DEEP_SLEEP` set to 0 (stays awake and dark): back on in the saved color |

- Any color button tapped while off also turns the costume back on, in that color.
- The **inner C** is always on while the costume is on, in a solid color. Only the **outer ring** has on/off and effects. See [disc-build.md](disc-build.md).
- The ring's on/off and effect are the disc's own. The cloak only follows the color.
- When the ring comes on with the costume, it sweeps around in about 0.4 s.

## Timing

- **Taps wait out the window.** After a tap, nothing happens until `TAP_GAP_MS` (350 ms) passes with no further tap, in case another is coming. The one exception is the last tap a button understands, which acts as soon as it's released: the 2nd tap on a color button, the 3rd on black.
- **Holds** act as soon as they're reached: `SHORT_HOLD_MS` (1 s) on a color button, `LONG_HOLD_MS` (3 s) on black.
- **Two buttons**: pressing a different button during the window ends the first sequence as taps. A second button pressed while one is held is ignored.
- **At power-on or wake**: a button still held from that press is ignored until it's released, so waking with black doesn't also toggle the ring.

A tap therefore takes about 350 ms + `APPLY_DELAY_MS` (50 ms) to show; a double tap takes about 50 ms after the second release. Tune `TAP_GAP_MS` on the breadboard: shorter feels snappier, but double and triple taps get harder to hit.

### State machine

```
IDLE ──press──▶ DOWN ──release──▶ GAP ──TAP_GAP_MS──▶ taps(n)
                 │  ▲               │
                 │  └─press same────┘   n + 1 (the last allowed tap fires on release)
             held long enough
                 ▼
               HELD ──▶ hold(n)        (1 s color button, 3 s black after 1 tap)
```

Practise on the breadboard with [ButtonsAndColors](../../ButtonsAndColors) step 3 (`pio run -e taps`), which uses the same buttons and gestures.

## Both Costumes: Messages

Not built yet. One new message:

| Message | Direction | Purpose |
|---|---|---|
| `SET_COLOR_GROUP` | disc → every board in the group | Scheduled color change for both costumes |

- **Group ID**: a new constant, `GROUP_ID`, shared by all four boards. Packets carry it, and boards outside the group ignore them.
- **Same scheme as `SET_COLOR`**: color, event id, time remaining and latency estimate, sent 3 times inside the 50 ms window ([latency-handling.md](latency-handling.md)).
- **Own cloak**: treats it like `SET_COLOR`.
- **Partner's disc**: schedules the change *and adopts the color as its own*, so its heartbeat keeps its cloak in sync afterwards.
- **Partner's cloak**: schedules directly from the same broadcast. It doesn't wait for its disc to relay, so all receivers line up on the same moment.
- **Latency to the other costume**: the sending disc reuses the latency it measured to its own cloak. It's the same kind of radio hop, so the error should be well under 1 ms.
- **Both send at once**: if both discs send within the same 50 ms window, the one from the lower `COSTUME_ID` wins on every board.
- **Out of range**: only your costume changes. A later addition could have the partner acknowledge, with a short blink if no acknowledgment comes back.

There is no "both off" gesture now. Black hold 3 s turns off your own costume only.

## Implementation Plan

1. ~~Four-button gestures, primary/secondary colors, outer ring on/off and effects~~ Built.
2. **`SET_COLOR_GROUP`**: add `GROUP_ID`; send from `requestBoth()`; receive on all roles with the tie-break; the partner disc adopts the color.
3. **Bench test** with `disc-1` + `disc-2` first (two boards, no cloaks), then all four.
4. **Dock sensor** (GPIO 3, [disc-build.md](disc-build.md)): outer ring off while on your back, ignite when pulled off.

## Decisions

- **Four buttons**: black 5, white 6, green 7, blue 10, lined up in that order. Black is the wake button.
- **Colors in pairs**: tap for the primary, double tap for the secondary.
- **Both costumes**: the 1 s hold versions of tap and double tap.
- **Off**: black hold 3 s, own costume.
- **Tap timing**: wait out the window, so all four boards change together on a "both" gesture.

# Electronics carrier plate — cut `12-electronics-carrier-plate-3mm.svg`

3 mm acrylic. Black = cut. **Blue = engrave only, never cut** — those are the board outlines,
the USB-C mouths and the labels, so you can see exactly where each board goes.

## What I used

| Board | Size | Mounting holes? |
|---|---|---|
| ESP32-C3 Super Mini | 18 × 22.5 | assume none |
| TP4056 charger | 17 × 28 | assume none |
| **MT3608 boost** | **32.8 × 17.8** — measured from your photo (1.29 × 0.70 in) | **none — those four big pads are wire pads** |

**No board is screwed down.** Each one is held by a **cable tie** through the pair of 1.8 × 14
slots either side of it, plus a square of foam tape underneath. That works whether or not
your boards have mounting holes, which is the thing I could not check.

## Orientation

Both USB-C ports sit on the **inner arc**, facing the hand hole, in the same direction —
marked `USB-C` on the engrave layer. The plate is a sector of the 300° bay, R72–R108, inset
2 mm off each bridge, so it drops into the bay and cannot be fitted the wrong way round.

Every board corner and every slot was checked against the plate outline: furthest is the
ESP32-C3 at R107.1, against a R108 edge.

## Four Ø3.5 holes

Two at the back and two between the boards at the front — screw the plate down to the back
carrier, or just foam-tape it if you are in a hurry today.

## Order of work

1. Cut the plate.
2. Lay the boards on the engraved outlines and check they match before anything is stuck.
3. Foam tape under each, then a cable tie through its two slots.
4. Wire it up on the bench, off the disc.
5. Drop the plate into the bay, USB ports toward the hand hole.

If your TP4056 is 26.5 long rather than 28, or the ESP32-C3 is a different Super Mini, tell
me the number and I will re-cut the file — it is one line.

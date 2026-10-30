# Electronics carrier — a structural mount, three layers of 3 mm acrylic

Cut all three. Black = cut, blue = engrave only.

| File | Qty | What it is |
|---|---|---|
| `12a-carrier-base-3mm.svg` | 1 | plain sector, the floor |
| `12b-carrier-pockets-3mm.svg` | 1 | same sector with a **press-fit pocket per board** |
| `12c-carrier-retainers-3mm.svg` | 8 | small tabs that stop a board lifting out |

## How the boards are actually held

**12b cements on top of 12a.** That makes a 3 mm-deep pocket shaped to each board. The board
drops in and is located on **all four sides by 3 mm of acrylic** — it cannot shift, rotate or
creep, and no board needs a mounting hole. Pockets are cut at board size **+ 0.2 mm**; the
laser kerf turns that into a snug push fit.

A notch at each USB end clears the connector body, so the board seats flat against the pocket
floor with the socket proud of the wall.

**Then two retainers per board.** Cement a tab from 12c across the pocket wall so it overhangs
the board edge by about 2 mm. Two per board and nothing lifts out. Each tab also has a 3.2
hole if you would rather use an M3 screw than cement.

That is the whole mount: pocket for position, tabs for retention. No cable ties.

## Pocket sizes

| Board | Size used | Pocket |
|---|---|---|
| ESP32-C3 Super Mini | 18 × 22.5 | 18.2 × 22.7 |
| TP4056 charger | 17 × 28 | 17.2 × 28.2 |
| **MT3608 boost** | **32.8 × 17.8** (measured from your photo) | 33.0 × 18.0 |

Walls between pockets are 8.8 and 11.8 mm, so the plate stays stiff.

## Orientation

Both USB-C mouths sit on the inner arc, facing the hand hole, in the same direction. The
plate is a sector of the 300° bay (R72–R108, inset 2 mm off each bridge) so it drops in and
cannot be fitted backwards. Every pocket vertex was checked against the plate outline.

## Order of work

1. Cut 12a, 12b and 12c.
2. **Dry-fit each board in its pocket in 12b before cementing anything.** If one is tight,
   a few strokes of a file on the pocket wall; if one is loose, say the real size and I will
   re-cut the file.
3. Cement 12b onto 12a, lining up the four mounting holes.
4. Drop the boards in, cement two retainers over each.
5. Wire it up on the bench, then screw the assembly to the back carrier with four M3.

## If a board does not match

Tell me the real measurement and the pocket is one line to change. The sizes for the ESP32-C3
and the TP4056 came from the project docs, not from your actual parts — only the MT3608 is
measured.

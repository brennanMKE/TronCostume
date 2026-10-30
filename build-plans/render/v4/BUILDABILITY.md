# Buildability audit — every physical assumption, checked or flagged

Written because two of my errors reached Brennan unchecked: following `frame.md` instead of
`disc-build.md`, and specifying LED strips lying flat when tape cannot bend that way. Both
were assumptions I never tested. This is the list I should have kept from the start.

## Verified

| # | Assumption | How it was checked | Result |
|---|---|---|---|
| 1 | A strip on edge can follow R93 and R110 | tape bends about its thickness, not in plane | **holds** — and flat does **not**, which is why that was wrong |
| 2 | Every component fits inside its bay | each corner tested against the bay boundary | holds, all five |
| 3 | All 13 fasteners land in solid wood | each one tested against the bay/bridge/rim regions | holds |
| 4 | Front screws miss the light channels | R96 against the solid R93–110 band | holds |
| 5 | Template apertures admit the bushing | narrowest is 42.76 vs 7.938 | holds |
| 6 | 18650 holder fits the bay | 21 mm holder, 24 mm bay | 3 mm clear |
| 7 | Front and back inserts never meet | 6 mm radially, z 15–25 vs 29–39 | 4 mm of wood between |
| 8 | **The frame is a constant cross-section** | every feature is a through-cut | **true — so the laser can cut it in layers** |

## Fixed by this audit

- **Ten hand-set inserts will not land perfectly.** The carrier's ten holes are now **Ø5.5**,
  not Ø4.5 — 1.5 mm of slop on an M4 shank, and a countersunk head still covers it. Ten
  exact holes meeting ten hand-drilled inserts was never going to go together.
- **The Ø8 wire tunnel no longer has to be drilled sideways through 24 mm of plywood.** With
  a layered frame it is a notch in one middle layer (file 11).

## Not verified — these depend on what you actually own

| # | Assumption | If wrong |
|---|---|---|
| 1 | **LED tape is 5 mm wide** | 10 mm will not stand in a 9 mm channel. Cut the channel layer at **12 mm**; nothing else changes. **Still unanswered.** |
| 2 | Plywood in 24 / 9 / 3 mm | the frame can be laminated from 8×3, 6×4, 4×6 or 2×12 |
| 3 | 9 mm white acrylic for the ring | three 3 mm rings cemented works |
| 4 | You own a bearing-guided flush-trim bit | only needed for the router route — the laser route does not use one |
| 5 | You have 13 M4 wood inserts | — |
| 6 | You have acrylic solvent cement | the C bar and the ring both depend on it |

## Known weak points, in order

1. **The white C bar.** Three pieces, each 6 mm wide and 504 mm long, cemented into one
   9 mm bar. Floppy to handle and hard to keep aligned. This is the highest fabrication risk
   in the build. Cut it last; cement it on a flat board with the pieces held against a
   straight fence; or use one piece of 9 mm white if you have it.
2. **Strip adhesive on a curved vertical wall.** It lets go. Add a dab of hot glue every
   50 mm.
3. **Protoboard in a 1.8 mm slot in 3 mm acrylic.** Only 3 mm of grip. Hot glue it.
4. **The channel walls must be painted white before anything goes in.** Easy to forget and
   impossible afterwards.

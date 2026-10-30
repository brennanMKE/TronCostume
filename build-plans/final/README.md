# Finalized build plans

Drawings here are the ones to build from. Anything not in this folder is a draft.

| File | Status | Covers |
|---|---|---|
| [FRAME-PLAN.png](FRAME-PLAN.png) | **REJECTED — do not build from this** | Lower frame: front view, back view, covered-bay detail |
| [FRAME-PLAN.svg](FRAME-PLAN.svg) | Vector source, 1:1 mm | Same sheet, for printing or measuring |

> **Rejected 2026-10-29 by Brennan.** The bay layout is wrong — see
> [Why the layout was rejected](#why-the-layout-was-rejected) below. The sheet is kept because its
> *insert placement*, *outer geometry* and *generator* are still correct and reusable; only the bay
> shapes have to be redrawn. Read that section before touching `frame_render.py`.

## FRAME-PLAN — what it is

The 4 × 6 mm maple plywood ring from [`docs/frame.md`](../../docs/frame.md), glued to 24 thick,
Ø260 outside / Ø120 hand hole. It fixes the thing Brennan asked for first: **where the wood
inserts go, front and back.**

- **Front inserts** — 3 × M4 at **R102**, on 0° / 120° / 240°, into the front face (z = 0).
  These take the face screws from [`docs/front-face.md`](../../docs/front-face.md).
- **Back inserts** — 3 × M4 at **R80**, same three angles, into the back face (z = 24).
  These take the carrier and back cover, still to be designed.
- **Block inserts** — 4 × M4 at bay x = ±46, axis radial, in the glued-in cover blocks.

Front and back sets are at different radii on purpose, so their screw tips can never meet.

It is **not an AI image.** Every arc, wall and hole is computed from the dimensions in
`frame.md` by [`../render/frame_render.py`](../render/frame_render.py), so it is safe to scale
off. Regenerate with:

```sh
cd build-plans/render
python3 frame_render.py && rsvg-convert -z 4 frame-plan.svg -o frame-plan.png
```

This sheet is a **layout and insert-placement drawing, not a cut file.** The laser file for the
four frame layers still has to be produced from it — `build-plans/halloween/` has cut files 1–7
for the face, C, outer ring, channel layer, floor, back ply and jigs, but nothing for the frame.

## One change to the frame against the spec

**The 0° wedge tip is relieved to R66.** Both covered bays run 106 wide all the way to the hand
hole, so their walls cross on the 0° axis at R61.20: the two openings merge and the wedge ends in
a zero-width knife point that will splinter. `frame.md` describes this as "a thin sliver of wood
… (R60 to about R65) — trim it off", which is the right instinct but the wrong number. The
drawing cuts a relief arc at **R66, ±6.58°, 15.2 mm long**, which leaves a blunt tip. R62 would
remove the cusp alone and still leave a 2.7 mm point.

`docs/frame.md` has not been edited. Make that edit once the relief radius is agreed.

## Two decisions still open

1. **Battery bay hand-hole wall is 6.0 mm** at 180°, the thinnest wood in the frame — 24 tall and
   cross-grain in two of the four layers. Moving the bay from y = 66 to y = 70 gives a 10 mm wall
   and still clears an 80 × 22 holder.
2. **Block inserts are tight.** The block is 14 wide and the protoboard slot takes 1.5 off its
   inner face, leaving 12.5 mm of wood. An 8 mm-OD insert at x = ±46 leaves only 1.5 mm to the
   slot. A 6 mm-OD hex-drive M4 insert gives 2.5 mm / 4 mm — use solid hardwood blocks, not
   laminated ply. Widening the block instead would make the two covered bays non-identical.

## Still to draw

Front face assembly, then the back face, carrier and the magnet mount that joins the cloak —
the back is not specified anywhere yet.


## Why the layout was rejected

Brennan's verdict: *"The frame layout is terrible. The openings for the battery charger and buttons
should be on the edge of the inner ring. They cannot be set back so far … Then you need to account
for channels for the LEDs."*  Reference photos are in [`mockup/`](../../mockup/).

### What is wrong

The sheet draws the bays straight out of `docs/frame.md`: a front part 106 wide from the hand hole
to y = 84, then a rear part 78 wide continuing all the way to **R114**. That eats almost the whole
radial width of the ring, leaves only three narrow wedges, and puts cutouts underneath the entire
LED channel region. `mockup/3 components.png` shows the real intent — every component hugs the
inner edge of the Ø260/Ø120 ring and the outer half stays solid.

### How deep the bays actually need to be

From the component sizes in `docs/disc-build.md`, measuring radially out from the hand hole at R60:

| Component | Size | Radial depth | Reaches |
|---|---|---|---|
| Protoboard on edge + 6×6×9.5 tactile switches | 80 × 20, 1.8 thick | ~12 | ~R74 |
| ESP32-C3 Super Mini, USB-C toward the hole | 18 × 22.5 | 22.5 | ~R83 |
| USB-C charger (TP4056), USB-C toward the hole | ~17 × 28 | 28 | ~R88 |
| MT3608 boost, lying lengthwise along the cover | 17 × 36 | 17 | ~R77 |
| 18650 as a straight chord | 18.5 × 67 bare | — | **~R92 at the ends** |

So **nothing needs to go past about R92**, against the R114 currently drawn. `disc-build.md`
already says as much for the electronics bay: *"the furthest corner reaches about R102, inside the
R110 outer rim."*  The rear part of each covered bay can be deleted outright.

### The LED channels that have to be accounted for

These live in the **upper** frame (z 3–13), above the floor, so they do not collide with the bays
in z — but the bays have to stop leaving them spanning open air, and wire drops have to land
somewhere useful:

| Feature | Radius | Note |
|---|---|---|
| C channel | R80–94 | C strip stands on the **R94 wall**, facing inward |
| Middle band | R94–110 | Light barrier. Face screws at R102 |
| Outer channel | R110–118 | Outer strip on the **R110 wall**, facing outward |
| White outer ring | R118–130 | — |

The 3 mm acrylic floor is all that spans a bay opening. A 106-wide hole under the C channel is a
lot of unsupported floor; shallower, narrower bays fix that too.

### Two conflicts between the docs, unresolved

1. **Channel radii.** `front-face.md` says C channel R79–93, strip on R93, middle band R93–110.
   `disc-build.md` says R80–94, strip on R94, middle band R94–110. One millimetre, but pick one
   before cutting.
2. **Battery holder.** `frame.md` specifies a holder (77–80 × 21–22 × 20 tall) in a 24 mm bay.
   `disc-build.md` says *"A cell holder (about 21 mm tall) doesn't fit the 18 mm bay"* and assumes a
   bare tabbed cell. The two docs assume different frame thicknesses. `mockup/3 components.png`
   shows a holder, so frame.md's 24 mm appears to be the live version.

### What is still good on the rejected sheet

- Insert placement: front R102, back R80, on 0°/120°/240°; block inserts at bay x = ±46.
- Outer geometry: Ø260, Ø120, outer rim, and the clock/angle convention.
- The audited corrections — 0° cusp at R61.20, cover setback 32.88, back-insert clearance 16.28.
- `../render/frame_render.py` is parametric; the bay shapes are a handful of constants
  (`COV_HALF`, `REAR_HALF`, `Y_STEP`, `BAT_*`) and the `covered_bay()` / `battery_bay()` functions.

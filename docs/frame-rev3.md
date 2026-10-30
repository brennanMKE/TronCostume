# Wood Frame — rev 3

> **DRAFT. Not approved, not for cutting.** This supersedes [frame.md](frame.md), whose
> bay geometry Brennan rejected on 2026-10-29. Drawings:
> `build-plans/render/frame-plan-v3.png` (front) and `frame-plan-v3-back.png` (back).
> Both are generated 1:1 from the numbers below — if a number here changes, regenerate.

The plywood ring that carries the three sets of components. Its measurements are the
reference for everything else.

- **The front** ([front-face.md](front-face.md)) screws into **3 inserts on its front side**.
- **The back** (carrier, back cover, magnet mount) screws into **3 inserts on its back side**.
- **The two covers** screw into **4 inserts in the frame itself**. There are no glued blocks.

## What changed from frame.md, and why

| rev 1 (rejected) | rev 3 |
|---|---|
| Bays were sectors running out to **R114** | Pockets sized to the components, nothing past **R100.7** |
| Cover was a 106-long chord; its ends finished **32.9 mm** behind the hand hole | Covers are short and flat; nothing you touch is more than **6 mm** back |
| Each bay ate **124°** of the hand hole | Buttons 66 mm of opening, electronics 76 mm |
| 4 glued 14×20×24 blocks held the cover screws | **No blocks.** The cover seats on a routed shoulder |
| 3 mm rebate for the cover ears | Deleted — **it cannot be routed**, see [Manufacture](#manufacture) |
| Wire slots: an arc per pair of bays, layer 4 only | **One 360° groove at R70** reaches all three pockets |
| Battery hand-hole wall 6.0 mm | 9.0 mm |

The root cause of rev 1 was putting flat parts on **chords** against a **round** hole. A
chord tangent to Ø120 runs away from it fast. Rev 3 keeps the flat parts short.

## Conventions

- **Units**: millimetres. **R**: radius from the disc centre. **Ø**: diameter.
- **Angles**: clockwise from 12 o'clock, **seen from the front**.
- **Frame z**: 0 at the front surface, 24 at the back.
- **Bay coordinates**: each bay has its own **x** and **y**. **y** is measured from the
  disc centre along the bay's centre line; **x** runs sideways, positive clockwise.
  A point (x, y) in a bay centred at angle A is at radius √(x² + y²) and angle A + atan(x / y).

## Overall

| | |
|---|---|
| Material | 24 mm maple plywood |
| Outside | Ø260 |
| Hand hole | Ø120 (R60) |
| Outer rim | R114 to R130, continuous, no openings |
| Bays | Buttons **60°**, battery **180°**, electronics **300°** |
| Wedges | Solid wood centred **0°, 120°, 240°** |

> **Open:** one 24 mm sheet routed, or four 6 mm layers laser-cut and glued? Rev 3 is drawn
> for the routed case. If it is four layers, the wire groove becomes a layer-4 cut instead.

## Manufacture

Routed against a laser-cut acrylic template with a **5/16" OD guide bushing** and a
**1/8" straight bit**. Cut files: `build-plans/render/template-acrylic-cut.svg` (cut this)
and `frame-pockets-finished.svg` (reference).

| | |
|---|---|
| Template offset | **2.38125** — every aperture is that much larger than the finished pocket |
| Finished inside corner | **R1.5875** if the 1/8" bit cuts the full wall — **but see below** |
| Minimum template aperture | **7.9375** (bushing OD) |
| Minimum finished pocket | **3.175** (bit) |

**Why there is no cover rebate.** A 3 mm-deep rebate for the cover ears needs a 7.76 mm
aperture; the bushing is 7.9375 and will not enter it. Instead the notch is cut to the full
cover width and the cover **seats on the shoulder** where the narrower pocket behind it
steps in — 6.41 mm of bearing each side after the corner fillet.

Registration: the template has a **Ø119.6 centre bore** for the existing jig plug
(`build-plans/halloween/7-jigs-ply.svg`) plus a **Ø6 pin at R80 / 180°**, which lands inside
the battery pocket and is routed away.

> **The 1/8" bit cannot cut the full depth.** 24 mm of ply plus a 3–6 mm template needs 27–30 mm
> of cutting length; common 1/8" bits give 12–25 mm and will deflect or snap long before that. So
> the template and bushing can only establish the top of the wall, and the depth has to be finished
> with a **bearing-guided flush-trim bit** riding the wall the template just cut.
>
> That changes the corner radius, because the flush-trim bit sets it: **1/4" → R3.175**,
> **1/2" → R6.350**, against the R1.5875 drawn here. **Which flush-trim bit do you have?**
> Every inside corner on the drawings and in the cut file has to be redrawn to match it.

> **Open:** are the pockets through-cuts or blind?

## Covered Bays

Both covers are **flat 3 mm black acrylic**, 23.5 tall (0.5 under the frame thickness so they
slide), screwed with M4 × 12 countersunk into inserts in the shoulder.

| | Buttons (60°) | Electronics (300°) |
|---|---|---|
| Notch, hole → y = 64 | \|x\| ≤ **35** | \|x\| ≤ **38** |
| Cover | **70** × 23.5 × 3 | **76** × 23.5 × 3 |
| Pocket behind | \|x\| ≤ **21**, y 64–84 | \|x\| ≤ **24**, y 64–87, then \|x\| ≤ **20**, y 87–92 |
| Shoulder (cover seat) | \|x\| 21–35 at y = 64, **14 wide** | \|x\| 24–38 at y = 64, **14 wide** |
| M4 inserts, axis radial | **Ø6** at x = **±28** | **Ø6** at x = **±31** |
| Pocket corner | R86.64 | R90.60 / R94.15 |

### Setback behind the hand-hole edge

Measured at each feature's own x, against the R60 arc. This is the number rev 1 got wrong.

| Feature | Behind the edge |
|---|---|
| Buttons at x = ±5.5 | 1.25 |
| TP4056 USB-C | 1.68 |
| ESP32-C3 USB-C | 2.43 |
| Buttons at x = ±16.5 | 3.32 |

| Notch ends | 12.26 (buttons) / 14.57 (electronics) |

The notch ends are the screw ears, with solid wood behind them — nothing is reached there.

### Buttons bay contents

- **Board 38 × 20**, standing on edge, four 6×6×9.5 tactile switches at **11 mm pitch**,
  x = −16.5, −5.5, +5.5, +16.5, tips through the cover.
- The 80 × 20 protoboard of rev 1 **does not fit**: a flat notch wide enough for it puts
  its ends 25.8 mm behind the hand hole.

### Electronics bay contents

Boards lie flat on the carrier, USB-C against the cover at y = 64.

| Board | Size | Place (bay x) |
|---|---|---|
| ESP32-C3 Super Mini | 18 × 22.5 | x = −21 … −3, USB-C at y = 64 |
| USB-C charger (TP4056) | 17 × 28 | x = +1 … +18, USB-C at y = 64 |
| MT3608 boost | 17 × 36 | **Stacked on standoffs over the TP4056** |
| Slide switch | 10 × 4 slot | **Moved out of this cover** — the shoulder needs the width. Location TBD |

**The MT3608 does not fit alongside** the other two in a 60-wide pocket. Stacking it costs
5 + 8 + 8 = **21 mm of the 24 mm** bay height.

> **Open:** MOSFET board dimensions unknown. **No space is reserved for it.**

## Battery Bay (180°)

| | |
|---|---|
| Pocket | \|x\| ≤ **41**, y **69–92**. Corners reach **R100.7** |
| Hand-hole wall | Solid from R60 to y = 69 — **9.0 mm** at the centre line. No cover |
| Holder | One 18650 holder, about 80 × 21 × 20 tall, lying as a chord |
| Access | From the back |

A cell is rigid, so this is the one thing that must stay a chord and the only pocket outside
R95. A bare tabbed cell (18.5 × 67, per [disc-build.md](disc-build.md)) would pull the
corners in to about R97.

> **Conflict:** frame.md assumes a holder in a 24 mm bay; disc-build.md says a 21 mm holder
> does not fit its 18 mm bay. The mockup photos show a holder, so 24 mm appears to be live.

## Inserts

| Set | Where | Count | Facing | For |
|---|---|---|---|---|
| **Front** | R102 at 0°, 120°, 240° | 3 | Into the front surface (z = 0) | Face screws |
| **Back** | R80 at 0°, 120°, 240° | 3 | Into the back surface (z = 24) | Carrier and back cover |
| **Covers** | Shoulder face at y = 64, bay x = ±28 / ±31 | 4 | Radially, toward the hand hole | Cover screws |

The cover inserts need a **14 mm shoulder**: a Ø6 bore in the 8 mm shoulder of the first rev 3
draft left 1 mm of wood each side. 14 mm gives 4 mm each side, which is why the pockets are
narrower than the component sizes alone would suggest and why the slide switch left the cover.

Front and back are at different radii, so their screw tips can never meet: 22 mm apart
radially, and z 0–10 against z 14–24.

## Wire Groove

**One groove at R70 centre line, 3.175 wide (a single bit pass), 6 deep, cut in the back face
for the full 360°.** R70 is the radius at which a constant-radius pass breaks into all three
pockets, so the whole harness runs in one trammel setup with **no template**.

| Clearance | |
|---|---|
| To the R80 back inserts | 4.41 |
| Wood to the hand hole | 8.41 |
| Wood left under the groove | 18 of 24 |

**Outer LED strip feeder:** its leads drop at R112 and nothing in the lower frame reaches
past R100.7, so one radial groove in the **front** face at **310°, R94–R114, 6 deep** carries
them into the electronics pocket. The C-strip leads drop at R86, already inside that pocket.

> **Open:** front-face.md puts the floor wire holes at R86 / 325° + 35° and R112 / 320° + 40°.
> With rev 3's pockets those angles no longer sit over an opening. Both C drops must land
> inside 265°–335° or 30°–90°, and the outer drop must line up with the feeder at 310°.

## Build Order

1. Cut the acrylic template on the laser. Check the Ø119.6 bore against the jig plug.
2. Cut the Ø260 blank and the Ø120 hand hole. Drill the Ø6 registration pin at R80 / 180°.
3. Register the template with the plug and the pin; rout the pockets and notches.
4. Trammel the R70 wire groove in the back face, and the 310° feeder in the front face.
5. Drill and set the 3 front inserts (R102), the 3 back inserts (R80), and the 4 cover
   inserts in the shoulders.
6. Cut both covers; countersink; check they seat on the shoulders before drilling the cover holes.

## Sizes at a Glance

| Item | Size or position |
|---|---|
| Frame | Ø260 / Ø120, 24 thick |
| Outer rim | R114 – R130 |
| Buttons | notch \|x\| ≤ 35, pocket \|x\| ≤ 21 y 64–84, cover 70 |
| Electronics | notch \|x\| ≤ 38, pocket \|x\| ≤ 24 y 64–87 + \|x\| ≤ 20 y 87–92, cover 76 |
| Battery | \|x\| ≤ 41, y 69–92 |
| Front inserts | R102 @ 0°, 120°, 240° |
| Back inserts | R80 @ 0°, 120°, 240° |
| Cover inserts | Ø6 at bay x = ±28 (buttons), ±31 (electronics), y = 64, in a 14 mm shoulder |
| Wire groove | R70, 3.175 wide, 6 deep, back face, 360° |
| Template offset | 2.38125 · corner R1.5875 |

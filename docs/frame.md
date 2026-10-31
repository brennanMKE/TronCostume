# Wood Frame

> **SUPERSEDED — 2026-10-29.** The bay geometry below was rejected: the bays run out to
> R114 and the covers are 106-long chords whose ends finish 32.9 mm behind the hand hole.
> Use **[frame-rev3.md](frame-rev3.md)** instead. This file is kept because other docs still
> link to it and because the conventions, the insert radii (R102 front, R80 back) and the
> overall Ø260 / Ø120 are unchanged.

The plywood ring that holds the three sets of components. Its measurements are the reference for everything else:

- **The front** ([front-face.md](front-face.md)) screws into **3 inserts on its front side**.
- **The back** (carrier, back cover, magnet mount; next doc) screws into **3 inserts on its back side**.
- **The two access covers** screw into **4 inserts in 4 wood blocks**, which you build first and glue in.

The covers work like the concept images `concepts/Inner-rim electronics module.png` and `concepts/Exploded vertical four-button plywood module.png`: a flat black cover in the hand-hole wall, held by two screws into wood blocks either side.

## Conventions

- **Units**: millimetres.
- **R**: radius from the disc center.
- **Angles**: clockwise from 12 o'clock, **seen from the front**.
- **Frame z**: 0 at the frame's front surface, 24 at its back.
- **Bay coordinates**: each bay has its own **x** and **y**.
  - **y** is the distance from the disc center along the bay's center line, so the hand hole edge is at y = 60.
  - **x** runs sideways, positive clockwise (seen from the front), 0 on the bay's center line.
  - A point (x, y) in a bay centered at angle A is at radius √(x² + y²) and angle A + atan(x / y).

## Overall

| | |
|---|---|
| Material | **4 layers of 6 mm maple plywood**, laser cut all the way through, glued and clamped |
| Thickness | **24** (measure your layers; "6 mm" ply is often 5.5-5.8) |
| Outside | Ø260 |
| Hand hole | Ø120 (R60), except where the two covers sit |
| Outer rim | R114 to R130 (16 wide), continuous, with no openings |
| Layers | All four identical, except layer 4 (the back one) also has the wire slots |

## Plan

```
 Seen from the front, 12 o'clock up

                         0°  ← front insert R102, back insert R80
               ELECTRONICS   ║   BUTTONS
               bay 300°      ║   bay 60°
               (10 o'clock)  ║   (2 o'clock)
                     ┌─cover─╨─cover─┐
       240° ═════════│   hand hole   │═════════ 120°
   (inserts R102,R80)│     Ø120      │ (inserts R102, R80)
                     └──── wall ─────┘
                          BATTERY
                          bay 180° (6 o'clock)
```

Between the three bays, the frame is solid wood: three wide **wedges** centered at **0°, 120° and 240°**. They're the three connecting points with the front and the back.

## Inserts in the Frame (M4 wood inserts)

| Set | Where | Count | Facing | For |
|---|---|---|---|---|
| **Front** | **R102 at 0°, 120°, 240°** | 3 | Into the front surface (z = 0) | Face screws, through the face, upper frame and floor ([front-face.md](front-face.md)) |
| **Back** | **R80 at 0°, 120°, 240°** | 3 | Into the back surface (z = 24) | The back (carrier and back cover) |
| **Cover blocks** | In the 4 blocks, at bay coordinates x = ±46, y = 64, z = 12 | 4 | Radially, toward the hand hole | Cover screws |

- **Front and back are at different radii**, so their screw tips can never meet. Each insert is 10 long, and the wood is 24 thick.
- **Edge clearance**: at R102 and R80 on the wedges, every insert has more than 15 mm of wood around it.

## Covered Bays (buttons at 60°, electronics at 300°)

Both are **identical**: the same shape, the same blocks and the same cover outline.

```
 One covered bay, seen from the front. The hand hole is at the bottom. Units are bay x / y.

   y = 107 ┐            ╭────────────╮   ← outer edge of bay: R114 (outer rim beyond)
           │            │            │
           │            │  rear part │   |x| ≤ 39
           │            │            │
   y = 84  ┤     ┌──────┤            ├──────┐
           │     │BLOCK │   middle   │BLOCK │   blocks: x = ±39 … ±53, y = 64 … 84
           │     │14×20 │   |x| ≤ 39 │14×20 │
   y = 64  ┤     ├──────┴────────────┴──────┤
   y = 61  ┤     │█████ COVER, 106 × 3 █████│   cover: x = −53 … +53, y = 61 … 64
           │     │                          │
           │      ╲    open to the       ╱     the hand hole curves away here, so the
   y = 60  ┘        ╲   hand hole       ╱       cover's ends sit up to ~33 mm back
           x:   −53  −39       0      +39  +53
```

### Bay cutout (through all 4 layers)

| Part | Shape |
|---|---|
| Front part | \|x\| ≤ 53, from the hand hole out to y = 84 |
| Rear part | \|x\| ≤ 39, from y = 84 out to R114 (about y = 107 at the corners) |

The cover has to come straight out into the hand hole, so the front part stays 106 wide all the way to the hole. At 0°, the two covered bays' openings nearly meet at the hole edge, leaving a thin sliver of wood between them (R60 to about R65). **Trim it off.** The floor and upper frame above keep the hand hole round from the front, and the wedge is 50+ mm wide by R80.

The step at y = 84, x = ±39 to ±53, makes a **pocket for each block**. The block sits against the side wall (x = ±53) and the back wall (y = 84). So with the cover screwed to the blocks first, gluing the blocks in places the cover exactly at y = 61, 1 mm behind the hand hole at its middle.

### Blocks (4: 2 per covered bay)

| | |
|---|---|
| Size | **14 wide (x) × 20 deep (y) × 24 tall (z)**, the full frame thickness |
| Material | Solid hardwood holds an insert best. Or laminate four 14 × 20 pieces of the 6 mm ply |
| Insert | One M4 insert in the block's **front face** (the face toward the hand hole), centered: 7 from the side, 12 from the top. Axis radial |
| Buttons bays only | A **protoboard slot** in each block's inner side face (the face at x = ±39): 1.8 wide, 1.5 deep, the full 24 tall, at the protoboard's y position (below) |

### Cover (2: one per covered bay)

| | |
|---|---|
| Material | **3 mm black acrylic** |
| Size | **106 long × 23.5 tall** (0.5 mm under the frame thickness, so it slides in and out) |
| Holes | **2 × Ø4.5, countersunk** on the front for flush M4 heads, at **x = ±46**, centered in the height |
| Screws | M4 × 12 countersunk: 3 mm of cover, then 9 mm into the insert |
| Buttons cover | Plus **4 button holes and 1 switch slot**, marked from the finished protoboard (default below) |
| Electronics cover | No other holes. Remove it to reach both USB-C ports |

### Buttons bay contents

- **Protoboard, 80 × 20**, standing on edge: 80 along x, 20 along z. Its ends sit in the two block slots, which are 81 apart, giving 0.5 mm play.
- **The buttons point at the hand hole, through the cover.**
- **Board position**: the board's front face sits at **y = 61 + switch height** (for 6 × 6 × 9.5 mm tactile switches, y = 70.5), so the button tips come out flush with the cover's front. **Cut the block slots at that y.**
- **Default hole layout on the cover** (black, white, green, blue, then the switch):
  - Buttons: Ø4 at x = −27, −9, +9, +27.
  - Switch: a 10 × 4 slot at x = +40, which sits over the block, so it's only usable if the switch is mounted on the cover itself. Otherwise move all of them to suit your board.
  - All centered in the height.

### Electronics bay contents

The boards lie **flat on the carrier** (the back sheet; next doc), with **USB-C ports against the cover**:

| Board | Size | Place (bay x, y) |
|---|---|---|
| ESP32-C3 Super Mini | 18 × 22.5 | x = −36 … −18, y = 64 … 87, USB-C at y = 64 |
| USB-C charger (TP4056) | 17 × 28 | x = −14 … +3, y = 64 … 92, USB-C at y = 64 |
| MT3608 boost | 36 × 17 | x = −18 … +18, y = 88 … 105 (rear part) |

That leaves room at x = +5 … +38, y = 64 … 84 for the wiring, the later MOSFET board and the Hall sensor.

## Battery Bay (180°)

| | |
|---|---|
| Cutout (through all 4 layers) | \|x\| ≤ 45, y = 66 … 96. Corners reach R106 |
| Hand-hole wall | Solid wood from the hole (R60) to y = 66. **No cover**; reach the battery from the back |
| Holder | One 18650 holder (about 77-80 × 21-22 × 20 tall), lying as a straight chord, 80 along x |
| Height | The 24 mm bay takes a holder up to about 23 tall, standing on the carrier |

## Wire Slots (layer 4 only)

Wires run between bays under the wedges, along the carrier:

- **Arc slots, R92 to R100**, cut through **layer 4 only** (6 deep from the back), joining each pair of neighboring bays.
  - Electronics ↔ buttons: across the 0° wedge.
  - Electronics ↔ battery: across the 240° wedge.
- They stay clear of the back inserts at R80 and the front inserts at R102.

## LED Wire Holes (in the floor above the frame)

The floor ([front-face.md](front-face.md)) gets Ø5 holes that drop into the bays' open areas:

| Strip | Floor hole | Lands in |
|---|---|---|
| Inner C | R86 at **325°** and **35°** | Electronics / buttons bay, between the blocks |
| Outer ring | R112 at **320°** and **40°** | Electronics / buttons bay, rear part |

## Build Order

1. **Blocks**: make the 4 blocks and set an insert in each.
2. **Covers**: laser cut both covers and countersink them. Screw each cover to its pair of blocks.
3. **Frame layers**: cut the 4 layers (layer 4 with the wire slots), glue and clamp them, aligned with 3 dowels or a jig through the hand hole.
4. **Glue in the cover assemblies**: wood glue on the blocks' outer side and back faces. Push them into their pockets with the cover screwed on. The pockets set the position.
5. **Frame inserts**: set the 3 front inserts (R102) and the 3 back inserts (R80).
6. **Protoboard**: slide it into its slots, check the buttons are flush with the cover, and adjust the board's y position if not.

## Sizes at a Glance

| Item | Size or position |
|---|---|
| Frame | Ø260 / Ø120, 24 thick, 4 × 6 ply |
| Outer rim | R114 – R130 |
| Wedges (connecting points) | Centered 0°, 120°, 240° |
| Front inserts | R102 @ 0°, 120°, 240° |
| Back inserts | R80 @ 0°, 120°, 240° |
| Covered bays | Centered 60° (buttons), 300° (electronics) |
| Cover | 106 × 23.5 × 3 black, at bay y = 61 – 64, screws at x = ±46 |
| Blocks | 14 × 20 × 24, at bay x = ±39 – ±53, y = 64 – 84, insert at x = ±46 |
| Battery bay | Centered 180°, \|x\| ≤ 45, y = 66 – 96 |
| Protoboard | 80 × 20, on edge, ends in block slots 81 apart, front face at y = 61 + switch height |

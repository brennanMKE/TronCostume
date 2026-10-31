# Disc Build: Look, Layers, Lighting and Back Mount

The build plan for the Tron Identity Disc: a black acrylic face with an inlaid white C, a 9 mm white acrylic outer ring, a laminated plywood frame, three electronics bays behind removable inner-rim covers, and a keyed magnetic back mount: a bar magnet in the disc meets one in a small black mount that fits a rectangular socket in the disc's back.

This doc is written so it can be handed to an image model (ChatGPT) to render an exploded view. All the geometry is spelled out in numbers. The [Render Brief](#render-brief-for-chatgpt) at the end has four separate prompts (exploded view, buttons close-up, assembled and worn, cross-section) and a list of mistakes from the first render to correct.

**Status: plan, not yet test-fitted.** Measure the real sheets, inserts and boards (see [Measure Before Cutting](#measure-before-cutting)) before making the cut files.

## Conventions

- **Units**: millimetres.
- **R**: radius from the disc center. **Ø**: diameter.
- **z**: depth from the front face. z = 0 is the front (lit) face and z increases toward the back.
- **Angles**: clockwise from 12 o'clock, **seen from the front**. 0° = 12 o'clock, 90° = 3 o'clock, 180° = 6 o'clock, 270° = 9 o'clock.
- **Front**: the lit face. **Back**: the face against the wearer.
- **Inner edge**: the wall of the center hand hole. **Outer edge**: the outside rim.

## What It Should Look Like

Based on the replica in `references/TRONDISC.COM ｜ Review by DA ｜ Tron Identity Disc [w5fwf7Fzw_M].mp4` (the best close-up) and the film clip.

- **A flat gloss-black annulus**, 260 mm across, with a 120 mm hand hole.
- **The inner C**: a 6 mm white band about 85 mm from the center, lit in the current color. One 20° gap, at 12 o'clock. **It is always on** while the disc is on, and **always a solid color**.
- **The outer ring**: the outside edge glows. It is **off while the disc is on your back** and lights when you pull the disc off, with effects that **rotate and flicker**. On the replica, separate LEDs show along the edge; ours should be smoother.
- **Eight short unlit white ticks** near the rim, at 30°, 80°, 100°, 150°, 210°, 260°, 280° and 330°. They come in near-pairs either side of 3 and 9 o'clock.
- **The back** is plain black. Nothing is lit on the back.
- **No visible screw heads.** Black countersunk screws sit flush and blend into the black acrylic.

## Lighting Behavior

| State | Inner C | Outer ring |
|---|---|---|
| On your back (docked) | Solid, current color | Off |
| Pulled off the back | Solid, current color | Lights all at once, then steady, flicker or motion (black button) |
| Off (hold 3 s) | Off | Off |

Outer-ring effects, all in the current color:

- **Rotate**: a brighter section travels around the ring, about 1 turn per second.
- **Flicker**: small random brightness dips, like the film's energy edge.

Both rings use the same color, picked with the three color buttons. The black button controls the outer ring: tap for on/off, double tap for flicker, triple tap for motion ([controls.md](controls.md)). The cloak follows the color as before.

**Docking detection**: a small Hall-effect sensor in the disc senses a small magnet in one of the mount's pegs. See [Back Mount](#back-mount-keyed-magnet).

## Layer Stack

| z (front → back) | Part | Material | Thickness |
|---|---|---|---|
| 0 – 6 | **Face** | Black acrylic | 6 (measure: "just under 6") |
| 0 – 12 | **C inlay and fin** | 4 × white acrylic C pieces, cemented into one stack | 4 × 3 = 12 |
| 6 – 15 | **Outer ring** | White translucent acrylic | 9 |
| 6 – 15 | **Upper frame** | Plywood | 9 |
| 15 – 18 | **Divider** | Plywood | 3 |
| 18 – 36 | **Lower frame** (bays) | Plywood (18, or 12 + 6) | 18 |
| 36 – 42 | **Back cover** | Black acrylic | 6 |

**Overall: about 42 mm thick, 260 mm across.** The thickness is set by the 18650 (18.5 mm) plus the 9 mm ring height. See [Weight and Thickness](#weight-and-thickness) for ways to make it thinner.

### Cross-section through the C and the outer ring

```
 R:  60            80 82  88   94           110     118   126 130
 z
 0   ┌──────────────────┐▒▒▒▒┌─────────────────────────────────┐        ← black face 6 (OD 252)
     │  black face      │▒C ▒│  black face                     │
 6   ├──────────────────┼▒▒▒▒┼──┬──────────────┬─────────┬─────┴───┐   ← ring top: 4 mm white
     │ upper frame      │▒fin▒  │ upper frame  │ ◀LED    │ white   │     border shows at R126–130
     │ (inner piece)    │▒▒▒▒ ◀▌│ (middle band)│▌  gap   │ ring 9  │   ← outer strip faces OUT
 15  ├──────────────────┴──────┴┴──────────────┴┴────────┴─────────┤     into the ring
     │ divider 3 (full annulus, wire holes)                         │
 18  ├────────┬──────────────────────────────────────────┬──────────┤
     │ cover  │  bay: electronics / buttons / battery    │ outer    │
     │ (inner │  (between the 3 bridges)                 │ rim      │
     │  edge) │                                          │          │
 36  ├────────┴──────────────────────────────────────────┴──────────┤
     │ back cover, black 6 (magnet socket cut through at 6 o'clock) │
 42  └──────────────────────────────────────────────────────────────┘

 ▒ = white acrylic   ◀▌ = LED strip standing on edge, LEDs facing sideways (arrow = light)
```

## Parts

### 1. Face: black acrylic, 6 mm

- **Shape**: OD 252 (R126), center hole Ø120 (R60). **One solid piece; the outer edge is an unbroken circle.**
- **C slot**, cut through: from R82 to R88 (6 mm wide), 340° long, from 10° clockwise to 350°. The **20° black bridge** centered at 12 o'clock keeps the face one piece.
- **Six countersunk holes** for M4 flat-head screws at R70 and R102, at 0°, 120° and 240° (the bridge angles).
- **Eight tick slots** (optional) at R114–R122, 2 mm wide, at the tick angles above, for thin white inlays. Or skip the slots and paint the ticks with a white paint pen.
- It sits on the upper frame and on the inner 8 mm of the outer ring (R118–R126), cemented to the ring.

### 2. C inlay and fin: four white C pieces, 3 mm each

- **Four identical C pieces** cut from the 3 mm white sheet: R82 to R88, 340°, same angles as the slot.
- **Cemented into one 12 mm stack.**
  - The **top two** sit inside the face's C slot, flush with the front face, so the C reads as a solid white inlay.
  - The **bottom two** hang 6 mm below the face into the C channel as a **light fin**. The C strip shines sideways into the fin, and the light travels up through the stack to the face.
- Sand the face side flush after cementing (the black sheet is just under 6 mm).

### 3. Outer ring: white translucent acrylic, 9 mm

- **Shape**: OD 260 (R130), ID 236 (R118), 12 mm wide radially.
- **Position**: z 6–15, directly under the face's outer edge.
  - The face covers R118–R126 (an 8 mm cement land).
  - **R126–R130 stays visible from the front as a 4 mm white border.**
  - The whole **9 mm outside edge** is white and glows.
- Lit from inside by the outer strip, which faces outward across an 8 mm air gap.
- If the 9 mm sheet is clear rather than white, frost it by sanding both curved faces, or line its inner face with a strip cut from the 3 mm white sheet.

### 4. Upper frame: plywood, 9 mm (z 6–15)

One piece, glued to the divider:

| Zone | R | Notes |
|---|---|---|
| Inner piece | 60 – 80 | Face screws at R70. Forms the top of the inner edge |
| **C channel** | 80 – 94 | Open, 340° from 10° to 350°. The fin hangs into it at R82–R88. The C strip mounts on the **R94 wall**, facing inward toward the fin |
| 12 o'clock bridge | 80 – 94 | 20° of solid wood under the C gap. Joins the inner piece to the middle band |
| Middle band | 94 – 110 | Face screws at R102. Its outer wall (R110) carries the **outer strip**, facing outward |
| **Outer channel** | 110 – 118 | Open air gap, all the way around, between the middle band and the outer ring |

Paint the channel walls and the divider's floor in the channels gloss white. Paint the C strip's wall black behind the strip so light only goes toward the fin.

### 5. Divider: plywood, 3 mm (z 15–18)

- A full annulus, OD 260, ID 120. It is the floor of both light channels and the ceiling of the bays, and it makes the frame a stiff box.
- **Wire holes**, Ø5:
  - Into the C channel at R92, at 347° and 13°, just inside the channel's two ends (350° to 10° is the solid bridge under the C gap).
  - Into the outer channel at R114, at 355° and 5°.
  - Add more where a bay needs to reach a strip.
- The outer ring sits on its outer edge (R118–R130).

### 6. Lower frame: plywood, 18 mm (z 18–36)

| Element | Geometry |
|---|---|
| Outer rim | R110 – R130, continuous |
| Bridges | Three, **24 mm wide**, at **0°, 120°, 240°**, from the inner edge (R60) to the outer rim |
| Bays | Three open bays between the bridges, centered at **60°, 180°, 300°**, from the module cover to the outer rim |
| Cover notches | Where each bay meets the hand hole: a flat notch for a removable inner-rim cover, with a wood **end block** at each end to take the cover's M4 inserts |

- Inserts for the back cover screws: at the bridges (R70 and R102) and in the outer rim at R122 (60°, 155°, 205°, 300°).
- **Magnet block**: at 6 o'clock the battery bay stops at R100 between 150° and 210°, leaving solid wood from R100 to the outer edge. The disc's bar magnet sits in a pocket in this block (see [Back Mount](#back-mount-keyed-magnet)).
- Inserts for the face screws: driven from the top of the upper frame at R70 and R102 on the bridge angles. The 10 mm insert passes through the upper frame into the divider; the bridge below backs it up.
- Seal all wood (shellac or sanding sealer). Paint the outside edge and the hand-hole wall satin black, or wrap them in black silicone tape.

### 7. Back cover: black acrylic, 6 mm (z 36–42)

- OD 260, ID 120. No light, no windows.
- **Ten countersunk M4 holes**:
  - 6 at R70 and R102, at 0°, 120° and 240°.
  - 4 at R122, at 60°, 155°, 205° and 300°. The usual 180° screw moves to either side of the socket.
- **Magnet socket**: a **65 × 15 mm rectangular window cut through** the back cover at 6 o'clock, long side running left-right. Its inner edge is at R104 and its outer edge at R119, so it's centered at R111.5. The disc's bar magnet sits flush in the wood at the bottom of this 6 mm deep socket, and the mount's key fits into it. See [Back Mount](#back-mount-keyed-magnet).
- **Battery relief**: a 1 mm deep pocket on the **inside** face under the battery (engraved), since the cell is 18.5 mm and the bay is 18.

### 8. Inner-rim modules (three bays)

**Where the covers are: on the hand-hole wall, inside the hole.** The covers are **not** on the outside edge of the disc. Each one stands upright in the wall of the 120 mm hand hole, with its outer face looking at the disc's center. You reach them with your fingers inside the hole, where you'd grip the disc. The outside edge of the disc has no covers, no holes and no openings at all.

Each cover is a **flat black acrylic plate**, 6 mm thick and 17 mm tall (z 18.5–35.5). Its 6 mm thickness runs radially, and its height runs front-to-back, the same direction as the disc's thickness. It spans a straight chord of the hand-hole wall and sits in a notch cut into the lower frame's inner edge, with its middle 1 mm behind the hole's circle. Two black countersunk M4 screws go through it **radially, pointing away from the center**, into M4 inserts in wood end blocks either side of the notch. Take the screws out and the cover comes off **into the hand hole**, exposing the bay behind it.

```
 One bay, seen from the front (face removed). The hand hole is at the bottom.

            outer rim R110–R130 (solid wood, no openings)
   ┌──────┬──────────────────────────────────┬──────┐
   │      │                                  │      │
   │bridge│        bay: boards / switches    │bridge│
   │ 24 mm│        / battery                 │ 24 mm│
   │      ├───┬──────────────────────────┬───┤      │
   │      │end│   COVER (black, 6 thick) │end│      │ ← stands upright in the
   └──────┴blk┴──────────────────────────┴blk┴──────┘   hand-hole wall
                 ◀── hand hole, Ø120 ──▶
                 (fingers reach the cover from here)
```

```
 Buttons bay, cut through its middle. The disc center is to the left.

  disc       hand hole       │cover│ protoboard (vertical)      outer rim
  center ◀── (air) ────── ●──┤ 6   ├─[switch]──┤                 │
                       button│     │           │                 │
                       tip   │     │           │                 │
              the button tips poke through the cover TOWARD the disc
              center, so you press them from inside the hand hole
```

| Bay | Center | Contents | Cover |
|---|---|---|---|
| **Electronics** | 300° (10 o'clock) | ESP32-C3 Super Mini, USB-C charger (TP4056), MT3608 boost on a 3 mm acrylic carrier; the Hall sensor; room for the later MOSFET board | 100 long. No holes: remove it to reach both USB-C ports (that also vents heat while charging) |
| **Buttons** | 60° (2 o'clock) | Protoboard standing on edge (15 mm tall), four 6×6 mm tactile switches facing the hand hole; power slide switch (2-3 A); spare room for later additions | 90 long. Four Ø4 holes for the actuators, left to right black, white, green, blue; one slot for the slide switch |
| **Battery** | 180° (6 o'clock) | One protected 18650 with solder tabs, in a wood cradle with foam, plus an inline fuse | 90 long, no holes. This is where your hand grips, so it has no buttons |

**Electronics bay layout.** The boards lie flat, parallel to the face, with each USB-C socket at the cover:

- **ESP32-C3 Super Mini** (18 × 22.5): USB-C toward the hole.
- **USB-C charger** (about 17 × 28): USB-C toward the hole.
- **MT3608** (17 × 36): lying lengthwise along the cover. It has no USB. Leave clearance for its inductor and adjustment screw.
- **Fit**: the furthest corner reaches about R102, inside the R110 outer rim.

**Buttons bay.** Use switches with long actuators (6×6 × 9.5-13 mm tall) so the tips sit flush with the cover's front face, or 0.5 mm behind it. They should be easy to find with a fingertip but hard to press by accident.

**Battery bay.** The bare tabbed cell is 18.5 × 67, lying as a chord from about R68 to R87; its ends reach R92. A cell holder (about 21 mm tall) doesn't fit the 18 mm bay. The cell stays in the disc and charges through USB-C.

### Wiring paths

- Everything electrical lives in the bays. The strips are reached through the divider holes, either side of the C gap at 12 o'clock.
- **Data**: GPIO 4 → 330 Ω → C strip in (350°, running counterclockwise round to 10°) → down into the buttons bay → up into the outer channel → outer strip around 360°. One data line, two segments.
- 5V and GND go to the start of each strip.

## LED Strips

- **Type**: 5 V WS2812B-compatible, **5 mm wide** (2020-size LEDs), bare (no silicone). The 10 mm strips are too tall for the 9 mm channel.
- **Density**: 120 LEDs/m if you can get it, for smoother rotation effects; 60/m works.
- **Both strips stand on edge** against a channel wall, PCB vertical, so they bend around the circle the easy way. **The LEDs face sideways**, out through the white acrylic.

| Strip | Wall | Faces | Length | LEDs at 120/m | at 60/m |
|---|---|---|---|---|---|
| Inner C | R94, 340° | Inward, onto the fin | 558 mm | 67 | 33 |
| Outer ring | R110, 360° | Outward, onto the ring | 691 mm | 83 | 41 |

At 120/m that's about 150 LEDs. `LED_MAX_MA` keeps the current within what the MT3608 and 18650 can supply.

## Fasteners

All are **black M4 countersunk (flat head, 90°)**, sitting flush in countersinks in the black acrylic, into **M4 wood inserts** (assumed 8 mm OD × 10 mm long; measure yours). One length covers almost everything: **M4 × 14** (6 mm acrylic + 8 mm of thread).

| Where | Count | Into |
|---|---|---|
| Face | 6 (R70 and R102 at 0°, 120°, 240°) | Inserts in the upper frame, backed by the bridges |
| Back cover | 10 (R70 and R102 at 0°, 120°, 240°; R122 at 60°, 155°, 205°, 300°) | Inserts in the lower frame |
| Module covers | 6 (2 per cover) | Inserts in the end blocks, axes pointing at the center |
| Mount face to base | 4 | Inserts in the mount's plywood base |
| Mount pegs | 2 | Through each peg into an insert in the base |

- **Edge clearance**: keep at least 4 mm of wood around each insert. That's why the middle band is 16 mm wide and the bridges are 24 mm.
- **Countersinking acrylic**: use a 90° countersink at slow speed and stop when the head sits flush. Tighten until just snug, because acrylic cracks around overtightened countersunk heads.
- The face and back inserts at the same angle and radius don't collide: the face ones sit at z 6-16 and the back ones at z 26-36.
- The outer ring has **no screws**. It's cemented to the face and clamped between the face and the divider. A screw through it would cast a shadow in the glow.

## Back Mount: Keyed Magnet

A small black **mount** worn on your back holds the disc. It has a raised rectangular **key** with a bar magnet in it. The key drops into a matching rectangular **socket** in the disc's back cover, where a second bar magnet waits. The key lines the two magnets up exactly and holds the disc square, so it can't twist or slide. Two **pegs** sit inside the disc's hand hole near the top and take some of the weight.

### Magnets

- **Two bar magnets, 60 × 10 × 5 mm**, the ones you have: one in the disc, one in the mount.
- **Polarity**: let the two magnets snap together and mark the faces that touch. Glue each magnet with its **marked face outward**. Then they attract when docked, and the disc can't go on the wrong way.
- **Glue with epoxy**, not just double-sided tape. Magnets this strong pulling against each other will slowly creep off tape. A dot of tape to position them, then epoxy, is fine.
- **Pull force**: a matched pair of these at a 0.5 mm gap is very strong, probably more than 10 kg straight off. That's too much to pull off easily, but you don't pull it straight off; see [Taking it off](#taking-it-off). If it's still too strong, set the mount's magnet 1-2 mm deeper. Every millimetre of gap weakens it noticeably.

### Disc side (socket)

```
 Back of the disc, seen from behind (from the wearer), 6 o'clock at the bottom

                    ╭──────── hand hole Ø120 ────────╮
                    │                                │
                    ╰────────────────────────────────╯
              ┌────────────── 65 ──────────────┐
              │ ┌──────────── 60 ────────────┐ │  15   ← socket, cut through
              │ │ disc magnet, flush in wood │ │        the 6 mm back cover
              │ └────────────────────────────┘ │
              └────────────────────────────────┘
                     R104 (top edge) – R119 (bottom edge)
```

| Item | Size | Where |
|---|---|---|
| Socket in the back cover | 65 × 15, cut through the 6 mm acrylic | 6 o'clock, R104–R119, long side horizontal |
| Magnet pocket in the wood | 60.5 × 10.5, 5.5 deep (magnet + glue) | Centered in the socket, in the lower frame's magnet block (R100–R130, 150°–210°) |
| Disc magnet | 60 × 10 × 5 | In the pocket, marked face out, flush with the wood |

The socket is 6 mm deep: the back cover's thickness, with the wood and magnet as its floor. Paint the wood floor black.

**Fit check**: the socket's corners reach R123.4, inside the R130 edge, and the battery's ends reach R92.8, clear of the R100 block. The back cover's 180° screw moves to 155° and 205° to make room.

### Mount

Made from your 6 mm maple plywood and black acrylic, all cut on the xTool:

```
 Mount, seen from the front of the disc (as if the disc were transparent)

              ┌───────────────────────┐  ← top, y = +62
              │        (●) (●)        │  ← two pegs, inside the hand hole
              │                       │
              │      ( hand hole )    │     90 wide
              │                       │
              │                       │
              │   ═══════════════     │  ← webbing slots (2)
              │                       │
              │  ┌─────────────────┐  │
              │  │ key + magnet    │  │  ← y = −111.5, fits the disc's socket
              │  └─────────────────┘  │
              │   ═══════════════     │  ← webbing slots (2)
              └───────────────────────┘  ← bottom, y = −126

 Side view (the disc docks from the right)

   wearer │ base: 2 × 6 maple ply │ black acrylic face 6 │ key 6 │ ← disc back cover
          │ (webbing slots)       │                      │magnet │
          │                       │ peg Ø12 × 30 ────────────────────▶ into the hand hole
```

| Part | Material | Size |
|---|---|---|
| **Base** | 2 layers of 6 mm maple plywood, glued (12 mm) | 90 × 188 rounded rectangle, corner R10. Four 27 × 4 webbing slots |
| **Face** | 6 mm black acrylic | Same outline as the base. Screwed to the base with 4 flush countersunk M4 screws into inserts |
| **Key** | 6 mm black acrylic, cemented to the face | **64.4 × 14.4**: 0.3 mm smaller each side than the 65 × 15 socket. A 60.5 × 10.5 window cut through it for the magnet. Centered at y = −111.5 |
| **Mount magnet** | 60 × 10 × 5 | In the key's window, epoxied to the face, marked face out. Its face sits about 0.5 mm below the key's top |
| **Pegs** | Five 6 mm maple discs, Ø12, glued into a 30 mm stack, or a Ø12 dowel | At x = ±9.2, y = +52.2 (R53 from the disc center, 10° either side of 12 o'clock), so both sit under the 12 o'clock bridge's wood. Each held by an M4 screw from the back of the base into an insert in the peg. Round over the tips |

Coordinates are in mm from the disc's center when docked, with y up.

- **Pegs**: they sit inside the hand hole, 1 mm below its top edge. When you're upright, the disc hangs on the key; if anything flexes, the hole's top edge settles onto the pegs. They also stop the top of the disc from swinging out when you bend over. At 30 mm long they stay inside the 42 mm hole and don't show from the front.
- **Through the hand hole**, the mount's black acrylic face shows. That's fine, since it matches the disc.
- **Fit**: laser kerf changes sizes by a few tenths of a millimetre. Before cutting the disc's back cover, cut a **test socket and key** from scrap acrylic. Adjust the key size until it drops in with a slight wiggle and no force.

### Wearing it

- **Harness**: two lengths of 25 mm webbing through the mount's slots. They form shoulder straps that cross on the chest, like a backpack.
- **The mount goes on the outside of the cloak.** Fabric can't go between the key and the socket: it's a 0.3 mm fit. Options:
  - Sew or bolt the mount to the cloak, with the harness underneath and the straps coming through two small slits in the cloak.
  - Wear the harness over the cloak, with straps in black webbing.
- Since the mount is hidden behind the disc, it can stay on all evening.

### Taking it off

1. **Tip the bottom of the disc away from your back.** This peels the magnets apart from one end instead of pulling them straight off, which takes much less force. The key slides out of the socket as you tip it.
2. **Lift the disc up and off the pegs.**

To put it back, hang the hole's top edge over the pegs, then swing the bottom in. The key finds the socket, and the magnets snap it home.

### Docking sensor

- **The disc can't use a Hall sensor near its own bar magnet**, because the sensor would always read "docked".
- Instead, a small **Ø6 × 3 magnet** goes in the top of the **peg at 350°** (seen from the front; it's the right-hand peg seen from behind), facing the hand-hole wall.
- A digital Hall sensor (DRV5032 or similar, 3.3 V, on **GPIO 3**) sits in a small pocket drilled into the 12 o'clock bridge from the electronics bay side, behind 1-2 mm of wood at the hand-hole wall, at 350°. That's about 3 mm from the peg magnet. Its wires run through the pocket into the electronics bay.
- The disc's bar magnet is about 165 mm away, too far to trigger it.
- **Docked**: the inner C stays lit and the outer ring goes dark. **Pulled off**: the outer ring ignites.

## Structural Checks

| Check | Value | OK? |
|---|---|---|
| Insert wood margin, middle band | (16 − 8) / 2 = 4 mm a side | Just |
| Insert wood margin, inner piece | (20 − 8) / 2 = 6 mm a side | Yes |
| Bridge width vs insert | 24 vs 8 OD | Yes |
| Face held at the inner edge | 3 screws at R70; the C slot only leaves the 20° bridge, so the fin cement and the screws together hold the inner piece | Yes |
| Electronics bay reach | furthest corner ~R102 < R110 | Yes |
| Battery in bay | 18.5 cell in 18 bay + 1 mm back pocket | Just |
| Battery chord ends | R92.8 < R100 (magnet block) | Yes |
| Socket corners | R123.4 < R130 | Yes |
| Disc's weight | Carried by the key in the 6 mm socket; the pegs catch the top | Yes |
| Divider | Full annulus ties the upper frame, lower frame and ring into a box | Yes |
| Ring support | Sits on the divider R118–R130, cemented to the face R118–R126 | Yes |

The weakest point is the inner hand-hole wall at the three cover notches, where only the 6 mm acrylic cover spans the opening. The upper frame, divider, face and back are continuous above and below each notch, so the ring as a whole stays stiff. Don't use the covers as handles.

## Weight and Thickness

Rough estimate:

| Part | Grams |
|---|---|
| Face, black 6 | 270 |
| Back cover, black 6 | 300 |
| Outer ring, white 9 | 100 |
| Plywood (upper, divider, lower) | 460 |
| Battery, boards, strips, wire | 100 |
| Screws, inserts, covers, magnet | 80 |
| **Total** | **about 1.3 kg** |

That's heavy for something worn on the back and thrown around. Options:

- **Thinner battery**: a flat LiPo (about 8 mm) instead of the 18650 lets the lower frame drop to 9-12 mm: about 35 mm thick and roughly 200 g lighter.
- **Lighter back cover**: 3 mm black acrylic with button-head screws saves about 150 g, but the heads won't be flush.
- **Lighter plywood**: lightening holes in the lower frame's outer rim, between inserts.

## Firmware and Pin Changes This Needs

- **Two LED segments** (built): the C (always on, solid) and the outer ring (on/off and effects). Still to do: keep the ring off while docked.
- **Dock sensor**: digital Hall sensor input on **GPIO 3**, a deep-sleep wake pin (GPIO 0-5) that's still free. It was going to be used for battery sensing; that's deferred.
- **Outer ring effects**: rotation and flicker, disc only. The cloak keeps following the color.
- The four-button gestures and outer ring effects are built ([controls.md](controls.md)). `MAIN_LEDS` (C) and `RING_LEDS` (outer ring) are in `include/config.h`; set them to the counts of the strips you buy.

## Measure Before Cutting

- Black sheet thickness ("just under 6"). It sets the C stack height and the screw lengths.
- Whether the 9 mm sheet is white translucent, and how much light it passes.
- Plywood thicknesses on hand (9, 3, 18 or 12 + 6).
- M4 insert OD, length and pilot hole size; countersunk screw lengths on hand.
- Board sizes: ESP32-C3 Super Mini, USB-C charger, MT3608.
- Tactile switch actuator height; slide switch size.
- 18650 cell with tabs: length and diameter.
- 5 mm LED strip: actual width, LED pitch, and brightness through the white acrylic. Build a 100 mm test channel first.

## How This Differs From the Earlier Plans

| Topic | Earlier (concepts / `build-plans/tron-identity-disc-build-reference.md`) | Now |
|---|---|---|
| Face | 2 mm black mask over a 6 mm white diffuser | **One 6 mm black layer**, white C cemented into it |
| Inner C | R69–R73, 4 mm, lit by the outer channel's light | **R82–R88, 6 mm** (replica proportions), own channel and strip |
| Outer light | 4 mm white border of the diffuser | **9 mm white ring** forming the outer edge, plus the 4 mm border |
| Channels | One continuous channel | **Two channels**: C and outer ring, strips on edge facing sideways |
| Strip | 10 mm, mounting unresolved | **5 mm**, standing on edge, LEDs sideways |
| Frame | One 24 mm routed core, open sectors | **Upper 9 + divider 3 + lower 18** laminated, closed box |
| Buttons | 4 (white, red, green, brightness) | **4: black (outer ring, off, wake), white, blue, green**; six colors as tap/double-tap pairs |
| Modules | Electronics + buttons on the inner rim | **Electronics, buttons and battery**: three inner-rim bays at 10, 2 and 6 o'clock |
| Back | Twist-lock idea, undecided | **Keyed magnet**: a 60 × 10 × 5 bar magnet on each side, the mount's key seated in a 65 × 15 socket in the disc's back, two pegs in the hand hole, and a docking sensor |
| Screws | Socket heads | **Black countersunk M4 × 14**, flush |
| SVG cut files | `build-plans/*.svg` | **Out of date** (C radius, face holes). Redraw after the render is approved |

## Render Brief for ChatGPT

### How to use it

Image models get much more right when each image shows **one thing**. Send these as **four separate requests**, one image each, in order. After each one, check it against the checklist for that request, and reply with only the items it got wrong.

Attach this document to every request. For request 2, also attach `concepts/Exploded vertical four-button plywood module.png` and `concepts/Inner-rim electronics module.png`. Those show the right *idea*: a flat black cover set into the hand-hole wall. They have only 4 buttons and the wrong colors; follow this document for those.

### What the first render got wrong

Paste this list with every request:

1. **Covers in the wrong place.** The three black inner-rim covers were drawn on the **outside edge** of the ring, covering nothing. They belong **in the hand-hole wall, inside the 120 mm hole**, facing the center, each closing one bay.
2. **Buttons buried.** The four buttons were drawn on a board lying flat inside a bay, facing up toward the face, where nobody can reach them. They are on a **vertical** protoboard directly behind the buttons cover, **pointing toward the disc center**, with their tips poking **through the cover's four holes into the hand hole**.
3. **Inner edge drawn as a continuous wooden ring.** In the 18 mm lower frame, the hand-hole wall is only wood at the three bridges and end blocks. At each bay it is **an opening closed by its black cover**.
4. **Face cut through at 12 o'clock.** The black face is **one solid piece** with an **unbroken outer edge**. The only opening besides the center hole is the thin C slot, whose single small gap is at 12 o'clock. Nothing else is cut at 12 o'clock, and there's no notch or tab on the outer edge.
5. **C far too wide.** The C is a **thin line**: 6 mm wide on a 260 mm disc, about 1/43 of the diameter, the same width as the face's thickness. It was drawn as a wide band.
6. **Back mount changed.** There is no round dock plate, boss or steel discs any more. The mount is a small black rectangular paddle with a raised rectangular key holding a bar magnet, which fits a rectangular socket in the disc's back at 6 o'clock, plus two pegs.
7. **Cross-section geometry wrong.** The layers are flat sheets stacked on top of each other, with no steps. Only the outer white ring reaches out to R130 above the divider.

### Request 1: exploded view

> Photoreal exploded assembly of the DIY Tron Identity Disc in the attached document. One image, no insets. Dark grey studio background. Viewed at a 3/4 angle from above the front, with the front face up and the parts spread along the disc's central axis, about 35 mm apart. Thin leader-line labels. Parts from top to bottom:
>
> 1. **Black acrylic face**: one solid gloss-black annulus, 6 mm thick, Ø252, hole Ø120. **Its outer edge is an unbroken circle.** One thin C-shaped slot, 6 mm wide, centered 85 mm from the center, running 340° with a single 20° solid black gap at 12 o'clock. Six small flush countersunk holes. Eight tiny white tick marks near the rim.
> 2. **White C**: a thin white acrylic C, 6 mm wide and 12 mm tall, exactly the shape of the slot, with the same single 20° gap at 12 o'clock.
> 3. **White outer ring**: translucent white acrylic, 9 mm thick, Ø260 outside, Ø236 inside: a narrow 12 mm band.
> 4. **Upper plywood frame**, 9 mm: a flat plywood annulus with two narrow open channels. The inner channel is C-shaped and about 85 mm out, with a thin 5 mm LED strip standing upright on its outer wall. The outer channel is round, at the frame's outer edge, with a thin 5 mm LED strip standing upright on the frame's outside wall, LEDs facing outward. Solid wood under the C's gap at 12 o'clock.
> 5. **Plywood divider**: a flat 3 mm plywood annulus, Ø260, hole Ø120, with a few small wire holes.
> 6. **Lower plywood frame**, 18 mm: a solid outer rim, and three 24 mm radial bridges at 12, 4 and 8 o'clock running from the outer rim to the hand hole. Three open bays between them:
>    - **10 o'clock**: three small boards lying flat (ESP32-C3 Super Mini, a USB-C charger board, an MT3608 boost board) on a clear acrylic carrier, their USB-C ports at the hand-hole side.
>    - **2 o'clock**: a vertical strip of protoboard standing just behind the hand-hole wall, with four tactile switches pointing toward the disc center.
>    - **6 o'clock**: one blue 18650 cell lying as a straight chord.
>
>    **At each bay, the hand-hole wall is an opening.** It is closed by a flat black acrylic cover (90-100 long × 17 tall × 6 thick) standing upright in that opening. In this exploded view, show each cover **pulled about 30 mm inward into the hand hole**, along its two dashed screw axes, which point radially toward the center. Show brass M4 inserts in the wood end blocks either side of each opening. The **buttons cover** has four small round holes, and the four switch tips (black, white, green, blue, left to right) line up with them. **The outside edge of the lower frame is solid wood with no covers.**
> 7. **Black acrylic back cover**: 6 mm, Ø260, hole Ø120, ten flush countersunk holes. At 6 o'clock, a **65 × 15 mm rectangular window cut through it**, long side horizontal, about 111 mm from the center. Through it you see a 60 × 10 mm bar magnet set flush in the wood of the lower frame.
> 8. **Back mount**, apart at the bottom: a small black rectangular paddle, 90 × 188 mm, made of 12 mm maple plywood with a 6 mm black acrylic face. On its face: a raised black acrylic **key**, 64 × 14 × 6 mm, holding a matching bar magnet, lined up under the disc's rectangular window. Two round pegs, Ø12 × 30 mm, near the paddle's top, which sit just inside the top of the disc's hand hole. Four webbing slots with black straps. The paddle spans from inside the hand hole down to the 6 o'clock socket.
>
> Don't: put covers or openings on the outside edge; make the C wide; cut the face anywhere at 12 o'clock except the C's gap; draw any LED strip lying flat; show raised or socket-head screws; light anything on the back.

**Check**:
- Covers in the hole, facing center.
- Buttons visible through the buttons cover, pointing at the center.
- Face one piece, with an unbroken outer edge.
- C thin, one gap at 12 o'clock.
- A rectangular socket at 6 o'clock in the back cover, and a rectangular paddle mount with a key and two pegs (no round plate).

### Request 2: buttons module close-up

> Photoreal close-up in the style of the attached module images, looking **from inside the hand hole** at the hand-hole wall at 2 o'clock, front face up. The wall is laminated plywood (9 + 3 + 18 mm) under the 6 mm black face. In the lower 18 mm, a flat black acrylic cover (90 × 17 × 6 mm) sits in a notch in the wall, held by two flush black countersunk M4 screws at its ends. Four small round holes in the cover, evenly spaced, with tactile switch tips flush with the cover face, colored black, white, green and blue from left to right, plus a small slide switch at the right end. A second view, exploded toward the viewer, shows the cover pulled out: the vertical protoboard behind it, the four switches pointing straight at the viewer through where the holes were, and brass inserts in the end blocks.

**Check**:
- The cover is in the hand-hole wall.
- The buttons point at the viewer (toward the center).
- 4 buttons in the right colors.
- Flush countersunk screws.

### Request 3: assembled and worn

> Two side-by-side photoreal images of the finished disc, at night:
>
> - **Left**, front view: a gloss-black disc, Ø260, with a Ø120 hole. A **thin** C line glows solid blue (#6FC3DF), 6 mm wide, about 85 mm from the center, with **one small gap at 12 o'clock**. The 9 mm outer edge and a 4 mm white border around the face glow blue. Eight small unlit white ticks. The face's outer edge is a perfect unbroken circle. The screws are invisible, or barely visible as flush black heads.
> - **Right**, worn: a person seen from behind, in a black hooded cloak, with the disc on their upper back, on the outside of the cloak, held square. Only the thin C is lit; the outer edge is dark. The mount is hidden behind the disc; only a little black shows through the hand hole.

**Check**:
- C thin, with one gap at the top.
- No notch or tab on the outer edge.
- Outer edge dark in the worn view.

### Request 4: cross-section

> A clean technical cutaway illustration (not photoreal) through the disc at 2 o'clock, the cut face shown flat. The disc center is to the left. Draw **flat layers stacked from the top**, exactly as in the document's "Cross-section through the C and the outer ring" diagram:
>
> - Black face, 6 mm.
> - White C, 12 mm tall: 6 mm inside the face's slot and 6 mm hanging below it as a fin.
> - Upper plywood frame, 9 mm, containing the C channel and the outer air gap.
> - The 5 mm C LED strip, upright on the C channel's outer wall, shining **sideways** into the fin.
> - The 5 mm outer LED strip, upright on the frame's outside wall, shining **sideways** across an 8 mm gap into the 9 mm white outer ring, which is the outermost part.
> - Divider, 3 mm.
> - Lower frame, 18 mm, with the buttons cover at the hand-hole (left) end and a switch poking through it to the left.
> - Back cover, 6 mm.
>
> Label each layer with its thickness, and draw arrows for the light.

**Check**:
- No steps in the layers.
- Strips upright, shining sideways.
- The buttons cover is at the left (hand-hole) end, with the switch tip poking out to the left.

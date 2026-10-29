# Disc Build: Look, Layers, Lighting and Back Mount

The build plan for the Tron Identity Disc: a black acrylic face with an inlaid white C, a 9 mm white acrylic outer ring, a laminated plywood frame, three electronics bays behind removable inner-rim covers, and a magnetic mount for wearing it on the back.

This doc is written so it can be handed to an image model (ChatGPT) to render an exploded view. All the geometry is spelled out in numbers. The [Render Brief](#render-brief-for-chatgpt) at the end is the prompt to paste.

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
| Pulled off the back | Solid, current color | Ignites: a sweep around from 12 o'clock in about 0.4 s, then steady, flicker or motion (black button) |
| Off (hold 3 s) | Off | Off |

Outer-ring effects, all in the current color:

- **Rotate**: a brighter section travels around the ring, about 1 turn per second.
- **Flicker**: small random brightness dips, like the film's energy edge.

Both rings use the same color, picked with the three color buttons. The black button controls the outer ring: tap for on/off, double tap for flicker, triple tap for motion ([controls.md](controls.md)). The cloak follows the color as before.

**Docking detection**: a small Hall-effect sensor in the disc senses a magnet in the back mount. See [Back Mount](#back-mount-magnetic-dock).

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
     │ back cover, black 6 (steel targets recessed in the outside)  │
 42  └──────────────────────────────────────────────────────────────┘

 ▒ = white acrylic   ◀▌ = LED strip standing on edge, LEDs facing sideways (arrow = light)
```

## Parts

### 1. Face: black acrylic, 6 mm

- **Shape**: OD 252 (R126), center hole Ø120 (R60).
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

- Inserts for the back cover screws: at the bridges (R70 and R102) and in the outer rim at R122 (60°, 180°, 300°).
- Inserts for the face screws: driven from the top of the upper frame at R70 and R102 on the bridge angles. The 10 mm insert passes through the upper frame into the divider; the bridge below backs it up.
- Seal all wood (shellac or sanding sealer). Paint the outside edge and the hand-hole wall satin black, or wrap them in black silicone tape.

### 7. Back cover: black acrylic, 6 mm (z 36–42)

- OD 260, ID 120. No light, no windows.
- **Nine countersunk M4 holes**:
  - 6 at R70 and R102, at 0°, 120° and 240°.
  - 3 at R122, at 60°, 180° and 300°.
- **Three steel target discs**, Ø20 × 2, recessed 2 mm into the **outside** face at R90, at 60°, 180° and 300°. Cement or epoxy them in, painted black.
- **Locating socket**: a blind hole Ø6.5, 4 mm deep, on the outside face at R86, 0°. It makes the disc dock in only one orientation.
- **Battery relief**: a 1 mm deep pocket on the **inside** face under the battery (engraved), since the cell is 18.5 mm and the bay is 18.

### 8. Inner-rim modules (three bays)

Each bay is closed toward the hand hole by a **flat black acrylic cover**, 6 mm thick and 17 mm tall (z 18.5–35.5). It is held by two black countersunk M4 screws into M4 inserts in the end blocks, with the insert axes pointing at the disc center. Its front face sits 1 mm behind the hand-hole circle at the middle. From inside the hole it reads as a flat black panel set into the curved wall, the way the module concept images show.

| Bay | Center | Contents | Cover |
|---|---|---|---|
| **Electronics** | 300° (10 o'clock) | ESP32-C3 Super Mini, USB-C charger (TP4056), MT3608 boost on a 3 mm acrylic carrier; the Hall sensor; room for the later MOSFET board | 100 long. No holes: remove it to reach both USB-C ports (that also vents heat while charging) |
| **Buttons** | 60° (2 o'clock) | Protoboard standing on edge (15 mm tall), four 6×6 mm tactile switches facing the hand hole; power slide switch (2-3 A); spare room for later additions | 90 long. Four Ø4 holes for the actuators, left to right black, white, blue, green; one slot for the slide switch |
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
| Back cover | 9 (R70 and R102 at 0°, 120°, 240°; R122 at 60°, 180°, 300°) | Inserts in the lower frame |
| Module covers | 6 (2 per cover) | Inserts in the end blocks, axes pointing at the center |
| Dock plate magnets | 3 | Inserts in the dock plate |

- **Edge clearance**: keep at least 4 mm of wood around each insert. That's why the middle band is 16 mm wide and the bridges are 24 mm.
- **Countersinking acrylic**: use a 90° countersink at slow speed and stop when the head sits flush. Tighten until just snug, because acrylic cracks around overtightened countersunk heads.
- The face and back inserts at the same angle and radius don't collide: the face ones sit at z 6-16 and the back ones at z 26-36.
- The outer ring has **no screws**. It's cemented to the face and clamped between the face and the divider. A screw through it would cast a shadow in the glow.

## Back Mount (Magnetic Dock)

A **dock plate** worn on your back. The disc's hole fits over a round boss on the plate, and magnets hold it on. You pull it straight off.

```
   side view (wearer's back on the left)

   back │ harness │ dock plate 9 ply │ boss Ø114 ×10 ──┐  disc
        │ straps  │ ● magnets        │   fits the      │  ┌──────────┐
        │         │   (flush)        │   Ø120 hole     │  │ steel ●  │ back cover
        │         │                  │                 │  │          │
```

- **Dock plate**: 9 mm plywood, **Ø220**, painted black. Four slots for 25 mm webbing (two shoulder straps that cross on the chest, like a backpack frame).
- **Boss**: Ø114 × 10, glued to the plate's center (a plywood disc, or stacked rings to save weight). It goes into the disc's 120 mm hole with 3 mm clearance. **The boss carries the disc's weight**, so the magnets only have to hold it against the plate.
- **Magnets**: 3 countersunk **pot (cup) magnets, Ø20, M4**, screwed flush into M4 inserts in the plate at R90, 60°/180°/300°, matching the steel targets on the disc.
  - Each holds roughly 2-3 kg through 2 mm of steel, paint and fabric, about 6-9 kg in total.
  - That's enough for a 1.3 kg disc when you bend over, and still easy to pull off by tipping one edge first.
  - Test, and add a fourth magnet if needed.
- **Locating pin**: Ø6 × 4 on the plate at R86, 0°, into the disc's back socket, so the C's gap always docks at the top.
- **Docking sensor**: a small Ø10 × 3 magnet in the plate at R90, 330°. A digital Hall sensor (DRV5032 or similar, 3.3 V) sits inside the electronics bay, against the back cover, at the same spot. It tells the firmware the disc is on your back, so the outer ring goes dark.
- **With the cloak**: wear the plate **under** the cloak and dock the disc **over** it. Magnets hold through thin fabric, and the boss pushes the fabric into the hole. Test with the actual cloak fabric. If it's thick, mount the plate on the outside of the cloak instead.

## Structural Checks

| Check | Value | OK? |
|---|---|---|
| Insert wood margin, middle band | (16 − 8) / 2 = 4 mm a side | Just |
| Insert wood margin, inner piece | (20 − 8) / 2 = 6 mm a side | Yes |
| Bridge width vs insert | 24 vs 8 OD | Yes |
| Face held at the inner edge | 3 screws at R70; the C slot only leaves the 20° bridge, so the fin cement and the screws together hold the inner piece | Yes |
| Electronics bay reach | furthest corner ~R102 < R110 | Yes |
| Battery in bay | 18.5 cell in 18 bay + 1 mm back pocket | Just |
| Battery chord ends | R92 < R110 | Yes |
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
| Screws, inserts, covers, steel | 70 |
| **Total** | **about 1.3 kg** |

That's heavy for something worn on the back and thrown around. Options:

- **Thinner battery**: a flat LiPo (about 8 mm) instead of the 18650 lets the lower frame drop to 9-12 mm: about 35 mm thick and roughly 200 g lighter.
- **Lighter back cover**: 3 mm black acrylic with button-head screws saves about 150 g, but the heads won't be flush.
- **Lighter plywood**: lightening holes in the lower frame's outer rim, between inserts.

## Firmware and Pin Changes This Needs

- **Two LED segments** (built): the C (always on, solid) and the outer ring (on/off and effects). Still to do: keep the ring off while docked.
- **Dock sensor**: digital Hall sensor input on **GPIO 3**, a deep-sleep wake pin (GPIO 0-5) that's still free. It was going to be used for battery sensing; that's deferred.
- **Outer ring effects**: ignition sweep, rotation and flicker, disc only. The cloak keeps following the color.
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
| Back | Twist-lock idea, undecided | **Magnetic dock** with a boss, steel targets and a docking sensor |
| Screws | Socket heads | **Black countersunk M4 × 14**, flush |
| SVG cut files | `build-plans/*.svg` | **Out of date** (C radius, face holes). Redraw after the render is approved |

## Render Brief for ChatGPT

Attach this document and the two module images (`concepts/Inner-rim electronics module.png`, `concepts/Exploded vertical four-button plywood module.png`) as style references, then paste the brief below as the prompt.

---

**Render a photoreal exploded view of a DIY Tron Identity Disc, plus three detail insets. Follow the dimensions in the document exactly; don't invent parts.**

**Main view**: an exploded assembly along the disc's axis, seen from a 3/4 angle above the front. Front face up, about 35 mm of space between layers, thin dashed lines showing the screw axes. Dark grey studio background. Label each part with a thin leader line. From top (front) to bottom:

1. **Black acrylic face**, gloss, 6 mm thick, OD 252, hole Ø120. A 6 mm wide C-shaped slot at R82–R88 running 340°, with a single 20° black bridge at **12 o'clock**. Six flush countersunk holes (R70 and R102 at 12, 4 and 8 o'clock). Eight tiny white ticks near the rim.
2. **White C stack**: four thin white acrylic C pieces (3 mm each) cemented into one 12 mm C, the same shape as the slot. Shown just below the face, lined up with the slot.
3. **White translucent outer ring**, 9 mm thick, OD 260, ID 236, glowing softly.
4. **Upper plywood frame**, 9 mm: a C-shaped open channel (R80–R94) with a thin **5 mm LED strip standing on edge on its outer wall, LEDs facing inward**; a solid wood bridge under the C gap at 12 o'clock; an outer band whose outside wall (R110) carries a second **5 mm LED strip standing on edge, LEDs facing outward**. The channel walls are painted white.
5. **Plywood divider**, 3 mm, a full flat annulus with small wire holes near 12 o'clock.
6. **Lower plywood frame**, 18 mm: an outer rim, three 24 mm radial bridges at 12, 4 and 8 o'clock, and three bays between them:
   - At **10 o'clock**: the ESP32-C3 Super Mini, USB-C charger and MT3608 boost lying flat on a clear acrylic carrier, USB-C ports facing the hand hole.
   - At **2 o'clock**: a vertical protoboard with four small tactile switches facing the hand hole, plus a small slide switch.
   - At **6 o'clock**: one 18650 cell in a wood cradle.
   - Each bay has a flat black acrylic cover (6 mm thick, 17 mm tall) set into a notch in the hand-hole wall, held by two black countersunk M4 screws into brass inserts in wood end blocks. The button cover has four small round holes with actuator tips in black, white, blue and green (left to right), plus a slot for the slide switch.
   - Brass M4 wood inserts are visible at the bridges and the outer rim.
7. **Black acrylic back cover**, 6 mm, OD 260, ID 120. Nine flush countersunk holes. Three small round steel discs recessed flush in the outside face at 2, 6 and 10 o'clock. A small locating hole at 12 o'clock.
8. **Dock plate** (furthest down, slightly apart): a black-painted 9 mm plywood disc, Ø220, with a raised Ø114 × 10 mm round boss that fits the disc's hole. Three flush round pot magnets matching the steel discs, a small locating pin at 12 o'clock, and four webbing slots with black straps leaving the frame.

**Inset 1, assembled front view** (dark room): black disc; the **inner C glowing solid blue (#6FC3DF)** with its gap at 12 o'clock; the **outer edge and the 4 mm outer border glowing blue**; flush black screw heads barely visible; white ticks.

**Inset 2, cross-section** through the C and the outer ring, at 2 o'clock, labeled as in the document's section drawing: face, C inlay plus fin, C strip on edge shining sideways into the fin, middle band, outer strip on edge shining sideways into the 9 mm white ring, divider, button bay with its cover, back cover. Show light arrows.

**Inset 3, worn**: the back of a person in a black hooded cloak. The dock plate is strapped on under the cloak; the disc sits on the outside of the cloak, held through the fabric by the plate's boss and magnets. Only the C is lit; the outer ring is dark.

**Don't**:

- Don't light the back.
- Don't show socket-head or raised screw heads anywhere: every screw is a black countersunk head flush with the acrylic.
- Don't put a slot through the face at 12 o'clock other than the 20° gap in the C.
- Don't draw strips lying flat around a circle.
- Don't use a full-size ESP32 dev board.
- Don't use more than one gap in the C.
- Don't show lit ticks.

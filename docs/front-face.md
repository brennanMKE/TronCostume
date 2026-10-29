# Front Face Assembly

Step 1 of the disc build: the lit front face, and just enough of the wood frame behind it to place the face's screws and keep the two lights apart. The back (carrier, back cover, magnet mount) comes next, in a separate doc.

This replaces the front-stack parts of [disc-build.md](disc-build.md): the face is now 3 mm black, the outer ring is 10 mm white, and the frame is cut all the way through rather than routed.

## Conventions

- **Units**: millimetres.
- **R**: radius from the disc's center. **Ø**: diameter.
- **Angles**: clockwise from 12 o'clock, **seen from the front**. 0° = 12 o'clock, 90° = 3 o'clock, 180° = 6 o'clock, 270° = 9 o'clock.
- **z**: depth from the front surface. z = 0 is the front, and z increases toward the back.

## What You See From the Front

```
            12 o'clock: the C's single 20° gap
                    ╭───╮
           ░░░░░░░░░╯   ╰░░░░░░░░░         ░ white C, R82–R88 (always lit)
        ░░                         ░░
       ░      ┌───────────────┐      ░     ■ black face, R60–R126
      ░       │   hand hole   │       ░
      ░       │     Ø120      │       ░    ▒ white outer ring: 4 mm border
       ░      └───────────────┘      ░        R126–R130 plus the 10 mm edge
        ░░                         ░░        (lit only sometimes)
           ░░░░░░░░░░░░░░░░░░░░░░░
     ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒   ← outer edge, Ø260
```

- **Black face**: 3 mm, flat, one piece, with an unbroken outer edge.
- **White C**: inlaid flush in the black, 6 mm wide, one gap at 12 o'clock. **Always lit** while the disc is on.
- **White outer ring**: 10 mm thick, under the black face's edge. It shows as a 4 mm white border around the face and as the whole outside edge. **Lit only sometimes** (outer ring on/off and effects).
- **Three black countersunk M4 screws**, flush with the face.

## Materials for This Step

| Material | Used for |
|---|---|
| Black acrylic, 3 mm | Face; frame light-barrier layer; floor |
| White acrylic, 3 mm | C inlay, plus 2 more C pieces for the light fin |
| White acrylic, 10 mm | Outer ring |
| Maple plywood, 6 mm | Upper and lower frame layers |
| M4 wood inserts × 3 | In the lower frame, under the face screws |
| M4 × 25 countersunk (flat head, 90°), black × 3 | Face screws |
| Acrylic cement (solvent type, e.g. Weld-On 4 or similar) | Joins the three acrylic parts into one face |

**Check before cutting**: shine a phone flashlight through the 3 mm black sheet. If any light comes through, the black isn't opaque enough to hide the strips. Use two layers, or paint the back black.

## Part 1: Black Face (3 mm black acrylic)

| Feature | Dimension |
|---|---|
| Outside | Ø252 (R126). An unbroken circle |
| Hand hole | Ø120 (R60) |
| C slot, cut through | R82 to R88 (6 mm wide), 340°, from 10° to 350°. A **20° solid bridge** at 12 o'clock (350° to 10°) keeps the face one piece |
| Screw holes | **3 × Ø4.5**, at **R102**, at **0°, 120°, 240°**. Countersink each from the front, 90°, to Ø8.4, so the M4 head sits flush |
| Ticks (optional) | 8 short marks at R114–R122, at 30°, 80°, 100°, 150°, 210°, 260°, 280°, 330°. **Use white paint pen, not inlays.** White acrylic there would sit over the outer ring's light and glow |

- **Countersinking 3 mm acrylic**: the cone is about 2.2 mm deep, leaving about 0.8 mm. That's fine because the plywood directly underneath supports it. Use a sharp countersink bit at slow speed, stop as soon as the head sits flush, and tighten the screws only until snug.
- **Cut order**: on the xTool, cut the C slot and the screw holes before the outside circle.

## Part 2: White C (3 mm white acrylic, 3 pieces)

| Piece | Shape | Purpose |
|---|---|---|
| **C inlay** × 1 | R82 to R88, 340°, from 10° to 350° (the same path as the slot) | Fills the slot flush with the front. This is the C you see |
| **C fin** × 2 | Identical to the inlay | Cemented under the inlay. Hangs 6 mm down into the C channel and catches the C strip's light from the side |

- **Same path, so it fits**: cut the inlay from the same vector path as the slot. The laser's kerf makes the slot a little bigger and the piece a little smaller, which leaves a gap of about 0.1-0.2 mm that the cement wicks into.
- The three pieces are cemented into one 9 mm stack: the inlay on top, then the 2 fin pieces.
- If the C turns out bright enough without the fin (try it in the [light test](#light-test-before-the-real-cut)), leave the fin out.

## Part 3: White Outer Ring (10 mm white acrylic)

| Feature | Dimension |
|---|---|
| Outside | Ø260 (R130) |
| Inside | Ø236 (R118) |
| Radial width | 12 |
| Thickness | 10 (measure the real sheet; see [Heights](#heights)) |

- The black face overlaps it from R118 to R126, an **8 mm cement land** all the way round.
- **R126 to R130 stays uncovered** as a 4 mm white border on the front, and the whole 10 mm outer edge is white.
- It is lit from inside by the outer strip, across an 8 mm air gap.

## Cementing the Face (one solid part)

Work upside down on a flat, clean surface: the face goes **front side down**, on a sheet of paper so the cement doesn't stick it to the table.

1. **Alignment plug**: cut a Ø119.6 disc from 6 mm plywood scrap. It fits through the hand holes and keeps everything concentric.
2. **C**: cement the inlay and the 2 fin pieces into one stack first. Let it set.
3. Lay the face **front down** with the plug through its hole. Drop the C stack into the slot from the back, inlay first. The table keeps it flush with the front. Run cement along both seams with a needle applicator. Let it set.
4. **Ring**: cut a second jig disc, **Ø235.6**, from plywood scrap, with a Ø120 center hole. Slide it onto the plug, on the face's back. Drop the outer ring around the jig, sitting on the face's back R118–R126. Run cement around the inner seam, where the ring meets the face. Let it set, then lift out the jig and plug.
5. **Result**: one solid face part. Black face, C flush in it with a 6 mm fin behind, and the white ring under the outer edge.

## Light Separation

The C is always on, and the outer ring is only on sometimes. When the ring is off, **no C light may reach it**, and the outer strip mustn't light the C either.

| Path | How it's blocked |
|---|---|
| C channel ↔ outer channel, sideways | The **middle band** (R93–R110), solid plywood and black acrylic, the full height of both channels |
| Through the floor of either channel | The **floor** is 3 mm **black** acrylic (opaque). It is not white, because white acrylic would carry light sideways from one channel to the other like a light pipe |
| Through the face | 3 mm opaque black face (do the flashlight test) |
| Into the bays below | Black floor, with only small wire holes |

Inside each channel, paint the walls the light bounces off, and the floor, **white** (or line them with white tape) for brightness. The barrier itself stays black.

## Frame Behind the Face (enough to place the screws)

### Stack

| z (front → back) | Layer | Material | Thickness |
|---|---|---|---|
| 0 – 3 | Face | 3 mm black acrylic, with the C inlaid | 3 |
| 3 – 13 | **Upper frame** (light channels) and **outer ring** (R118–R130) side by side | Upper frame: 6 mm maple ply + 3 mm black acrylic + about 1 mm shim | 10 (= ring) |
| 13 – 16 | **Floor** | 3 mm black acrylic, full annulus | 3 |
| 16 – 40 | **Lower frame** (the three bays) | 4 × 6 mm maple ply | 24 |
| 40 – 43 | **Carrier** (the components bolt to it; details in the back doc) | 3 mm acrylic | 3 |

About **43 mm**, plus whatever the back adds.

### Heights

The **upper frame and the outer ring both sit on the floor** and both touch the face, so **they must be the same height**. Otherwise the face rocks or bows.

- Measure the white ring sheet (about 10). Make the upper frame match: 6 mm ply + 3 mm black acrylic is 9, plus a shim layer (cardstock or thin card) to make up the difference.
- Measure with calipers, since "6 mm" plywood is often 5.5-5.8.
- The 3 mm black acrylic layer inside the upper frame helps the light barrier, but it isn't required. Anything that makes up the height is fine.

### Upper frame (z 3–13): plan

One piece, cut identically in each of its layers:

| Zone | R | Notes |
|---|---|---|
| Inner piece | 60 – 79 | Under the black inside the C |
| **C channel** | 79 – 93 | Open, 340° (10° to 350°). The C fin hangs into it (R82–R88, 6 mm deep). The **C strip** stands on edge on the **R93 wall, facing inward** at the fin |
| 12 o'clock bridge | 79 – 93 | 20° solid (350° to 10°), under the C's gap. It joins the inner piece to the middle band, so the upper frame is one piece |
| **Middle band** | 93 – 110 | Solid. The **light barrier**. Face screws pass through it at R102. Its outer wall (R110) carries the **outer strip**, standing on edge, **facing outward** |
| **Outer channel** | 110 – 118 | Open air gap, 360°, between the middle band and the white ring |
| (Outer ring) | 118 – 130 | The 10 mm white ring, part of the face assembly |

Strips: 10 mm-wide WS2812B strips fit standing on edge in the 10 mm height.

### Floor (z 13–16): 3 mm black acrylic

- Annulus, Ø260 outside, Ø120 hole.
- **3 × Ø4.5 screw holes** at R102, 0°/120°/240°.
- **Wire holes, Ø5**:
  - C channel: R86 at 325° and 35°.
  - Outer channel: R112 at 320° and 40°.
  - Each drops into a bay's open area ([frame.md](frame.md)). Run the strip's leads along the channel to reach them.

### Lower frame (z 16–40): the three bays

Defined exactly in **[frame.md](frame.md)**: 4 × 6 mm maple ply, Ø260 / Ø120, with three bays.

| | |
|---|---|
| Buttons bay | Centered at 60°, with a black cover in the hand-hole wall |
| Battery bay | Centered at 180°, solid hand-hole wall |
| Electronics bay | Centered at 300°, with a black cover |
| Wedges | Solid wood at 0°, 120° and 240° |
| **Front inserts for the face** | **R102 at 0°, 120°, 240°** |
| Back inserts | R80 at 0°, 120°, 240° |

## Face Screws

```
 At R102 on each bridge (0°, 120°, 240°)

 z 0   ┌─ countersunk M4 head, flush ─┐  face (3, black)
 z 3   │ Ø4.5 clearance               │  upper frame middle band (10)
 z 13  │ Ø4.5 clearance               │  floor (3, black)
 z 16  ├── M4 insert, top flush ──────┤  lower frame bridge (24 ply)
       │   (10 long)                  │
 z 26  └──────────────────────────────┘
```

- **Screw**: **M4 × 25** countersunk. It passes 16 mm through the face, upper frame and floor, leaving 9 mm of thread in a 10 mm insert.
- If your inserts are 8 mm long, use M4 × 22.
- The three screws **clamp the whole front stack together**: face, upper frame, floor and lower frame.
- **Clearance holes** in the upper frame (every layer) and the floor: Ø4.5 at the same three spots.

## Light Test Before the Real Cut

Cut a short straight test piece from scrap (an hour, at most):

1. A 100 mm strip of 3 mm black with a 6 mm slot; a white inlay with 2 fin pieces cemented in.
2. Underneath, a 14 mm-wide, 10 mm-deep channel from ply scraps, painted white inside, on a black acrylic floor. Put a 10 mm strip on edge on one wall, facing the fin.
3. Beside it, a 10 mm white ring offcut with a strip facing it across an 8 mm gap, and the ply barrier between the two channels.
4. Run both in blue, then turn the "outer" strip off. **Check**: the C is even (no dots); no C light shows on the ring piece; no ring light shows in the C.

## Cut List for This Step

| Part | Material | Qty |
|---|---|---|
| Black face | 3 mm black | 1 |
| C inlay + fin | 3 mm white | 3 |
| Outer ring | 10 mm white | 1 |
| Upper frame layer | 6 mm maple ply | 1 |
| Upper frame layer | 3 mm black | 1 |
| Floor | 3 mm black | 1 |
| Lower frame layers | 6 mm maple ply | 4 |
| Jigs: plug Ø119.6, ring jig Ø235.6 with Ø120 hole | ply scrap | 2 |

The lower frame layers can be cut now for the insert positions, but their bay shapes depend on the back doc. Cut the face, C, ring, upper frame and floor first.

## Render Brief (face assembly only)

To check the look with ChatGPT, attach this file and paste:

> Photoreal exploded view of **only these four parts**, stacked along the central axis, front up, dark background, labeled:
> 1. A flat **gloss-black acrylic annulus**, 3 mm thick, Ø252, hole Ø120. Its outer edge is an **unbroken circle**. One **thin C-shaped slot**, 6 mm wide, centered 85 mm from the center (much closer to the outer edge than the hole), running 340° with a **single 20° black gap at 12 o'clock**. Three flush countersunk screw holes at 12, 4 and 8 o'clock, 102 mm from the center.
> 2. A **thin white acrylic C**, 6 mm wide and 9 mm tall (three 3 mm layers), the exact shape of the slot, with the same single gap at 12 o'clock.
> 3. A **white acrylic ring**, 10 mm thick, Ø260 outside, Ø236 inside: a narrow band.
> 4. Inset: the three parts cemented together, front view, the thin C glowing blue (#6FC3DF), and the 4 mm white border and outer edge glowing blue.
>
> Don't add any other parts, a second gap, a notch in the outer edge, or a wide C.

# Tron disc — build plan v4

**Everything here is decided.** Where there was a real choice I picked one and said why at
the bottom. Cut files are in this folder, 1:1 mm, black = cut, blue = engrave (never cut blue).

Ø260 overall · Ø120 hand hole · **42 mm thick**

---

## 1 · The stack

| z | Part | Material | File |
|---|---|---|---|
| 0–3 | **Top plate** — black face + white C inset + white outer ring | 3 mm acrylic | 1, 2, 3 |
| 3–12 | **Channel layer** — both LED channels | 9 mm plywood | 4 |
| 12–15 | **Divider** — full annulus | 3 mm plywood | 5 |
| 15–39 | **Frame** — 3 bridges, 3 open bays | 24 mm plywood | routed, 7 + 9 |
| 39–42 | **Carrier / back** — everything mounts to this | 3 mm acrylic | 6 |

The **divider** is what makes this rigid. It is a full unbroken annulus glued between the
channel layer and the frame, so the whole disc is a closed box rather than a stack of rings.

**Screws — 13 in total.**

- **Front, 3 × M4 × 16 countersunk at R96** (0°/120°/240°), through the top plate, channel
  layer and divider into inserts in the frame's front face. R96 sits in the channel layer's
  solid R91–117 band, so it never breaks into a light channel.
- **Back, 10 × M4 × 12 countersunk** into inserts in the frame's back face: **R70 and R102
  on each bridge** (6) plus **R122 at 60° / 155° / 205° / 300°** in the outer rim (4). This
  is `disc-build.md`'s documented pattern — Codex caught that my earlier three-screw version
  was invented rather than read. The four rim screws are what clamp the outer rim down.

Front R96 and back R102 share an angle but are 6 mm apart radially, and their inserts are
z 15–25 against z 29–39, leaving 4 mm of wood between. Checked, all 13 land in solid wood.

---

## 2 · Cut list

| File | Material | Qty | Notes |
|---|---|---|---|
| `1-top-black-3mm.svg` | black acrylic 3 | 1 | R60–118, C slot, 3 countersunk |
| `2-top-white-C-3mm.svg` | white acrylic 3 | 1 | same path as the slot — kerf leaves the cement gap |
| `3-top-white-ring-3mm.svg` | white acrylic 3 | 1 | R118–130 |
| `4-channel-9mm-ply.svg` | plywood 9 | 1 | both channels cut through |
| `5-divider-3mm-ply.svg` | plywood 3 | 1 | full annulus + 4 wire holes |
| `6-carrier-3mm-acrylic.svg` | acrylic 3 | 1 | all component mounting |
| `7-router-template-acrylic.svg` | acrylic 4–6 | 1 | **the template** |
| `9-od-guide-disc-acrylic.svg` | acrylic 4–6 | 1 | outside guide for the Ø260 |
| `8-frame-finished-REFERENCE.svg` | — | — | reference only, do not cut |

**Plywood blank for the frame: 24 mm, at least 280 × 280.** If you do not have 24 mm, glue
up **18 + 6** or **2 × 12** first and rout the laminated blank as one piece. The frame
thickness is the only dimension that depends on your stock.

---

## 3 · Routing the frame

Offset is **already in the files** — 2.38125 mm for your 5/16" bushing with a 1/8" bit. Do
not add compensation in xTool.

1. Drill the three **R96** holes through the 24 mm blank. They hold both templates and later
   take nothing — they end up inside solid bridge wood.
2. Screw **template 7** to the blank through those holes. Rout the hand hole and the three
   bays. A 1/8" bit will not reach 24 mm, so take it **8–10 mm deep only**.
3. Swap to a **bearing-guided flush-trim bit**, bearing riding the wall you just cut, and
   take the rest of the depth in two passes. Corners finish at that bit's radius — anywhere
   from R3 to R6 is fine, nothing seats in a corner.
4. Screw **disc 9** to the blank through the same holes and run the bushing **around its
   outside** to cut the Ø260 perimeter. Same two-stage depth.
5. Drill **Ø8 through each bridge at R90**, square across the 24 mm width, mid-thickness.
   Only the **0° bridge** hole is strictly needed — the five button wires run from the bay at
   60° to the bay at 300°, which crosses that one bridge. Drill all three anyway; they cost
   nothing and leave you room to re-route later.
6. Set the inserts: **3 × M4 in the front face at R96**; **10 × M4 in the back face** at R70
   and R102 on each bridge and at R122 on 60/155/205/300.

> In template 7 the two upper bays run into the hand hole, so their outlines cross it. Those
> crossing segments are inside the waste and fall out. Cut every line once.

---

## 4 · The top plate — one flat 3 mm plane

Three pieces, all 3 mm, all cemented edge to edge into a single disc:

- **Black** R60–118 with a C-shaped slot at R82–88, 340°, solid bridge at 12 o'clock.
- **White C** dropped into that slot.
- **White ring** R118–130 butted to the black's outer edge.

Lay them face-down on paper over a flat board, push the joints tight, and run solvent cement
into the seams with a needle applicator. The laser kerf leaves roughly 0.1–0.2 mm at each
joint, which is exactly what the cement wants.

---

## 5 · Lighting — both strips lie flat, facing up

| Strip | Sits in | Lights |
|---|---|---|
| C strip | C channel, R79–91 | the white C above it |
| Ring strip | outer channel, R117–127 | the white outer ring above it |

Both strips lie **flat on the divider, LEDs pointing up** at the white acrylic 9 mm above.
Paint the channel walls and floor white first. Feed both through the four Ø8 holes in the
divider at 352° and 8°, either side of the C's gap, down into the electronics bay.

This is deliberately simpler than edge-lighting with a fin. If you can see individual LEDs
through the white, drop a second strip of 3 mm white acrylic or a layer of baking paper into
the channel on top of the strip.

---

## 6 · The carrier — build the electronics off the disc

Everything mounts to file 6 and goes in as one unit:

| Bay | On the carrier |
|---|---|
| **Electronics 300°** | ESP32-C3 and TP4056 with **both USB-C mouths at the hand hole**, MT3608 beside them. M3 standoffs in the 3.2 holes |
| **Buttons 60°** | Protoboard stands **on edge** in the 1.8 × 82 slot. Four 6×6×9.5 switches at x = −27, −9, +9, +27 pointing at the hand hole |
| **Battery 180°** | 18650 holder on two M3 screws. Inner rim is solid here — this is where you grip |

**Button wiring, 5 wires:** one common ground plus one per switch. Run them from the button
board through the **Ø8 hole in the 0° bridge** into the electronics bay — 60° → 0° → 300°
crosses exactly one bridge. The carrier has a 9 mm hole over that bridge so the bundle is
never pinched between acrylic and plywood. Use a 5-way JST-XH or Dupont strip so the
carrier still lifts out as one wired assembly.

Assemble and test the whole carrier on the bench. Then screw it to the frame with three M4.

---

## 7 · Assembly order

1. Rout the frame, drill the three bridge holes, set six inserts.
2. Cut and cement the top plate.
3. Glue the **divider to the frame** (wood glue, clamp). Permanent.
4. Paint the channels white. Lay both strips, feed the leads down through the divider.
5. Glue the **channel layer to the divider**. Permanent.
6. Build and test the carrier, all three bays.
7. Drop the carrier on, 10 × M4 from the back.
8. Top plate on, 3 × M4 countersunk from the front.

---

## 8 · Decisions I made for you

| Decision | Why | If you disagree |
|---|---|---|
| **24 mm frame, 18650 in a holder** | Your mockup photo shows a plastic holder, and a holder is ~21 mm — it will not fit an 18 mm bay. Soldering tabs to a bare cell the night before a build is a bad trade. Laminate 18+6 or 2×12 if you lack 24 mm stock | Drop to 18 mm and a bare tabbed cell; total becomes 36 mm |
| **Strips flat, facing up** | Edge-lighting with a fin is two more parts and a test cut you do not have time for | Dotting is the risk; add a diffuser layer in the channel |
| **Top plate all one 3 mm plane** | This is what you described — inset white into black and fuse | A thicker white ring under the black edge is stronger but no longer flat |
| **No inner-rim covers** | The two service bays open straight into the hand hole, so buttons and both USB ports are directly reachable. Fewer parts, no end blocks, no chisel work | Add 3 mm black cover plates later; nothing stops you |
| **Bays R72–R110 (battery) / R50–R110 (the other two)** | Keeps solid rim where your hand grips, opens it where you need access | — |
| **Wires through Ø8 bridge holes** | One drill per bridge beats routing grooves | — |

## 9 · Not resolved

- **Plywood thickness you actually have.** Everything assumes 24 / 9 / 3. The frame is the
  only one that matters and it can be laminated, so this should not block you.
- **Magnet mount for the cloak.** Not designed. The back carrier has room at 6 o'clock
  outboard of the battery, R100–130, which is where `disc-build.md` puts it.
- **MOSFET board.** No space reserved; dimensions unknown.

# Disc CAD status

Where the disc's CAD stands as of 30 October 2026, so the build can be picked up in a new session. The deadline is Halloween, 31 October.

This replaces the older plan in [disc-build.md](disc-build.md) and [frame.md](frame.md), and the numbers in `cad/params.md` and `cad/out/`. Treat those as superseded.

## Where things are

- **Model source**: [`cad/disc.py`](../cad/disc.py). Every dimension is a named parameter at the top. Run it in the build123d-mcp server with `execute_file`; it registers every part with `show()` under the names below.
- **Cut and model files**: `cad/`, named by material and thickness. Every new export goes in `cad/`.
- **3D board** (interactive viewer with part checkboxes and saved views): https://claude.ai/artifact/3A6JtVC7az48z8ki9Cb69A. Source in `cad/viewer/`.

## The stack

All mm. Angles are clockwise from 12 o'clock, seen from the front. Outside diameter 260, hand hole 120.

| Layer | Height | Part | Shape |
|---|---|---|---|
| Back | −3 to 0 | Black acrylic, 3 | Full ring, with a window at 6 o'clock for the battery holder |
| 1–3 | 0 to 15 | Maple, 5 each | Bays: inner wall R60–R66, outer wall R120–R130, ribs 20 wide at 0°, 120°, 240° |
| 4–5 | 15 to 25 | Maple, 5 each | LED layers: wood out to R107, C channel R80–R96 |
| Ring | 15 to 25 | White acrylic, 10 | R110–R130, beside layers 4–5 and flush with them on top |
| Face | 25 to 28 | Black acrylic, 3 | R60–R114, overlapping the white ring 4 mm as a cement land |
| C | 25 to 28 | White acrylic, 3 | R82–R88, inlaid flush in the face, 20° gap at 12 o'clock |

**Total thickness 31 mm.** The outer edge of maple layers 1–3 gets sanded and colored with a black acrylic pen.

### Layer details

- **Layer 1**: the bays, plus the battery socket, the insert-block sockets and a 1.5 mm slot for the bottom edge of the button protoboard.
- **Layer 2**: same as layer 1 without the board slot, plus a half wire slot through the 12 o'clock rib.
- **Layer 3**: a full wire notch through the 8 o'clock rib, and the other half wire slot at 12 o'clock. The two half slots overlap 6 mm so wires drop between them while the rib stays whole in each layer.
- **Layer 4**:
  - Three bridges across the C channel at 0°, 120° and 240°.
  - The battery pocket.
  - The 1.5 mm slot for the protoboard's top edge.
  - It cuts as **two pieces**: the small piece behind the board slot, about 600 mm², glues under layer 5.
- **Layer 5**: one bridge, at 12 o'clock, inside the C's gap.

### LEDs

| Strip | Where it sticks | Height | Length |
|---|---|---|---|
| Outer, full circle | The R107 wood wall, shining outward into the inner edge of the white ring | 17.5–22.5 | About 691 mm |
| C | The R96 wall of the C channel, top half only so it clears the battery | 20–25 | About 570 mm |

### Battery

- The holder is 80 × 21 × 22, at 6 o'clock, lying along the ring with its center at R81.
- It sits in the back window, flush with the outside, from −3 to 19. That leaves a 1 mm gap to layer 5 and to the C strip.
- It's held by a 0.25 mm-clearance socket in layers 1–3 plus glue.
- **The 22 mm height is the binding limit.** With the holder sitting on the back instead, it's 2 mm too tall for the 20 mm under layer 5.

### Bay covers

There are two covers, both 3 mm black acrylic standing in the hand-hole wall, set 1 mm behind the R60 circle. Buttons are at 2 o'clock (60°), USB at 10 o'clock (300°).

- **Size**: the main part is 90 long and 24.5 tall. Tabs reach out to 116 long, but only in the bottom 14.5 mm.
- **Screws**: 2 × M4, 4.5 mm clearance holes in the tabs, 101 mm apart, 7.5 mm up.
- **Inserts**: they go in glued blocks you make yourself, **12 × 12 × 15 mm**, sitting in sockets in layers 1–3. An insert 8 mm across and 10 mm long is assumed. Measure yours.
- **Buttons**:
  - 4 holes 4 mm across, 15.24 mm apart, 10 mm up.
  - The protoboard is 80 × 20 × 1.6. It stands on the back acrylic in the 1.5 mm slots in layers 1 and 4, a light press fit.
  - At 6.5 mm total switch height the tip is flush with the cover's front; 7 mm switches stick out 0.5 mm.
- **USB cover**: no button holes. The charger and ESP32-C3 lie flat behind it with their USB-C ports facing it.

## Cut files

| File | Sheet | Note |
|---|---|---|
| `acrylic-3mm-back` | Black 3 | |
| `maple-5mm-layer1` | Maple 5 | |
| `maple-5mm-layer2` | Maple 5 | |
| `maple-5mm-layer3` | Maple 5 | |
| `maple-5mm-layer4` | Maple 5 | Two pieces |
| `maple-5mm-layer5` | Maple 5 | |
| `acrylic-10mm-white-outer-ring` | White 10 | |
| `acrylic-3mm-black-face` | Black 3 | |
| `acrylic-3mm-white-c` | White 3 | |
| `acrylic-3mm-cover-buttons` | Black 3 | |
| `acrylic-3mm-cover-usb` | Black 3 | |

- **Formats**: each part has an `.svg` and `.dxf` at 1:1 in mm. The SVGs use 0.1 mm red (#FF0000) cut lines.
- **3D files**: each part also has a `.step` and `.stl`, and `disc-assembly.step` holds the whole stack.
- **Reference models (not for cutting)**: `battery-holder-reference.stl`, `protoboard-reference.stl`, `insert-blocks-reference.stl`, `led-outer-strip-reference.stl` and `led-c-strip-reference.stl`.
- **No kerf allowance yet.** Cut a test piece first.

### Re-exporting after a change

1. Run `cad/disc.py` with `execute_file`.
2. Use `export` with `filename` set to the full path in `cad/`:
   - `<name>_outline` objects export as `dxf,svg`.
   - Solids export as `step,stl`.
   - The assembly is the `result`.
3. Turn the SVG lines red:
   `sed -i '' 's/stroke="rgb(0,0,0)" stroke-width="0.4"/stroke="#FF0000" stroke-width="0.1"/' cad/<file>.svg`
4. Update the 3D board:
   1. Run `python3 -I cad/viewer/stl_to_json.py <stl basename> ...`.
   2. Republish `cad/viewer/index.html` to the board's URL, with the changed `models/*.json` files.

## Proposed next: open it up for service

You need to reach the components and swap the battery once the wood is glued. The plan, not yet modeled:

- **Lid**: the face, white C, white ring and maple layers 4–5, with both LED strips stuck on. Glued and cemented into one piece.
- **Base**: the back and maple layers 1–3, holding the battery, charger, ESP32, protoboard and insert blocks. Glued into one piece.
- **Screws**: 6 × M4 through the face at the bridges (0°, 120°, 240°), at R72 and R103. They thread into inserts in the base's ribs. Length about M4 × 25.
- **LED connection**: one 3-pin connector (5 V, ground, data) between lid and base. The C strip feeds the outer strip.
- **Opening it**: lift the lid and every bay is open from the top. The bay covers stay with the base, and the protoboard stays in its layer 1 slot.
- **Checked against the current model**:
  - **Base**: an insert 8 mm across and 10 mm long, set into the base from its top, lands fully in solid wood at all six spots (R72 and R103 at 0°, 120° and 240°). It clears the bay notches, the insert-block sockets and the wire slots.
  - **Lid**: a 4.5 mm screw hole at R72 is in the inner wood (R60–R80), and one at R103 is in the wood between the channels (R96–R107). Neither crosses the C channel or the white C.

To model the split, add to `cad/disc.py`:
1. 4.5 mm clearance holes through the face and layers 4–5.
2. Insert holes, sized to the measured insert, in layers 1–3.
3. A countersink note on the face, or button-head screws.
4. A reference connector in a bay.

## Open questions

Measure these before the final cut:

1. **The real thickness of the maple**: it's "about 5".
2. **The xTool model.** Diode lasers struggle with 10 mm white acrylic. If it can't cut the ring, stack thinner white sheet or have it cut elsewhere.
3. **The M4 insert's hole size**, and its outside size and length.
4. **Countersunk or button-head M4 screws** for the face. A flush head leaves only about 0.7 mm of the 3 mm face, and it has to be countersunk by hand.
5. **The battery**: keep the window (31 mm thick), or add a sixth maple layer (36 mm) so the holder screws down on a solid back.
6. **The battery holder's real size**: its length including the end tabs, its height (23 mm is the most that fits), and the size of its screw hole.
7. **The tactile switches' total height.**
8. **Wire notches** at the battery socket's ends for the holder's leads. Not added yet.

## Build order for 31 October

1. Finish the lid split in CAD.
2. Test-cut the kerf, insert hole, C inlay and board slot.
3. Cut all parts.
4. Glue the base and lid, and let them dry overnight.
5. Electronics: both strips, the connector, the protoboard, the charger, the ESP32 and the battery. The firmware is already in `src/main.cpp`.
6. Fit everything and fix what needs it.

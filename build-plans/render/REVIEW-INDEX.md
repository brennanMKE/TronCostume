# Tron lower frame — Claude review set

**DRAFT throughout. Nothing here is approved and nothing is ready to cut.**
Everything is generated 1:1 from one set of constants, so the sheets, the cut files
and the spec cannot disagree with each other.

## Open these in this order

| # | File | What it is |
|---|---|---|
| 1 | **frame-plan-v3.png** | Front view + a detail per bay. The main sheet. |
| 2 | **frame-plan-v3-back.png** | Back face: back inserts and the wire routing. |
| 3 | **frame-sections.png** | Radial sections. The only views that place things in **z**. |
| 4 | **frame-rev3.md** | The written spec, matching the above. |
| 5 | **cut-files/template-acrylic-cut.svg** | The routing template. Laser this in acrylic. |

Also here: matching 1:1 SVGs, and the generators (`frame_render_v3.py`,
`frame_render_v3_back.py`, `frame_section.py`, `cut-files/template_cut.py`).

`FRAME-PLAN-V2.*` is superseded — it had faceted covers, which you rejected.

## The design in six lines

- **Flat covers**, short, sized to their own features. Nothing you touch is more than
  6 mm behind the hand-hole edge — buttons 1.25 and 3.32, USB-C 1.84 and 1.93.
- **No blocks.** The cover seats on a **14 mm shoulder** where the narrower pocket behind
  it steps in. M4 **Ø6** inserts drill into that shoulder face at bay x = ±28 and ±31.
- **Component-sized pockets.** Buttons \|x\| ≤ 21, y 64–84. Electronics \|x\| ≤ 24,
  y 64–87 then \|x\| ≤ 20 to 92. Nothing past R94 except the battery.
- **Battery** \|x\| ≤ 41, y 69–92, no hand-hole opening, 9 mm wall, reached from the back.
- **One wire groove** at R70, 3.175 wide, 6 deep, 360°, cut with a trammel. It reaches all
  three pockets in a single pass and needs no template.
- **Inserts**: front R102, back R80, both at 0° / 120° / 240°.

## Five things I need from you

1. **Which flush-trim bit do you have?** A 1/8" bit cannot reach 24 mm of ply plus the
   template, so the depth has to be finished with a bearing-guided flush trim, and that bit
   sets the finished corner radius. Drawn at **R3.175 (1/4")**, which works. **1/2" does
   not** — it would force the electronics pocket out to \|x\| ≤ 25.35 and cut the shoulder
   back to 12.65.
2. One routed 24 mm sheet, or four 6 mm layers glued?
3. Bays through-cut or blind pockets?
4. MOSFET board dimensions — **no space is reserved for it.**
5. Where does the slide switch go? It came out of the electronics cover when the shoulder
   had to widen, and has no home.

## Things I changed that you should know about

- Button board is **38 × 20** with the switches at **11 mm pitch**. The 80 mm protoboard
  cannot be used: a flat notch wide enough for it puts its ends 25.8 mm behind the hole.
- **MT3608 stacks on standoffs over the TP4056** — it does not fit alongside. 5 + 8 + 8 =
  21 mm of the 24 mm bay height.

## Known weak points, measured not guessed

| | |
|---|---|
| Floor bridging the electronics pocket | 27 mm unsupported, 1.30 mm deflection, **SF 2.9** — the thinnest margin in the build |
| Cover insert vs wire groove | **3 mm** in z, and only because the groove is 6 deep from the back |
| Covers themselves | SF ~8. Not a concern; an earlier flag of mine was wrong |

## Still unresolved between the existing docs

- `front-face.md` and `disc-build.md` disagree by 1 mm on the C-channel radii.
- `front-face.md`'s floor wire holes (R86 / 325°+35°, R112 / 320°+40°) no longer sit over an
  opening with these pockets — they would drop into solid wood.

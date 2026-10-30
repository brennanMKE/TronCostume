#!/usr/bin/env python3
"""Sheet 3 — radial sections through the disc, showing the z stack.

Two cuts: one down a covered bay's centre line, one through a wedge. Together
they place every feature in z, which the plan views cannot show.
"""
import math
from frame_render_v3 import Sheet, INK, MAPLE, BLUE, RED, GREEN, GREY, MAG, BIT

# overall z, measured from the front of the face (front-face.md stack)
FACE = (0, 3); UPPER = (3, 13); FLOOR = (13, 16); FRAME = (16, 40); CARRIER = (40, 43)
R0, R1 = 54.0, 136.0
SX, SZ = 3.9, 3.9                      # mm of sheet per mm of part

BLACK_AC, WHITE_AC, PLY = "#2a2a2a", "#f2f2f2", MAPLE


class Sec:
    def __init__(self, sh, ox, oz, title, sub):
        self.sh, self.ox, self.oz = sh, ox, oz
        sh.text(ox + (R1 - R0) * SX / 2, oz - 11, title, 5.4, INK, weight="700", ls="1.2")
        sh.text(ox + (R1 - R0) * SX / 2, oz - 6, sub, 3.3, "#555")
    def X(self, r): return self.ox + (r - R0) * SX
    def Z(self, z): return self.oz + z * SZ
    def box(self, r0, r1, z0, z1, fill, stroke=INK, w=0.6, dash=None, op=1.0):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.sh.add(f'<rect x="{self.X(r0):.2f}" y="{self.Z(z0):.2f}" '
                    f'width="{(r1-r0)*SX:.2f}" height="{(z1-z0)*SZ:.2f}" fill="{fill}" '
                    f'fill-opacity="{op}" stroke="{stroke}" stroke-width="{w}"{d}/>')
    def lbl(self, r, z, s, size=3.2, col=INK, anchor="middle", w="400"):
        self.sh.text(self.X(r), self.Z(z), s, size, col, anchor=anchor, weight=w)
    def tick(self, r, s):
        x = self.X(r); z0 = self.Z(-2); z1 = self.Z(45.5)
        self.sh.add(f'<path d="M {x:.2f},{z0:.2f} V {z1:.2f}" stroke="{GREY}" '
                    f'stroke-width="0.25" stroke-dasharray="2,2"/>')
        self.sh.text(x, z1 + 4, s, 3.0, GREY)


def common(s, cut_frame):
    """Everything that is the same in both sections. cut_frame = list of (r0,r1) voids."""
    s.box(60, 126, *FACE, BLACK_AC)                       # face
    s.box(118, 130, 3, 13, WHITE_AC)                      # white outer ring
    s.box(60, 79, *UPPER, PLY); s.box(93, 110, *UPPER, PLY)   # upper frame, C + outer channels open
    s.box(60, 130, *FLOOR, BLACK_AC)                      # floor
    s.box(60, 130, *CARRIER, "#dfe9f0")                   # carrier
    solid, r = [], 60.0
    for a, b in cut_frame:
        if a > r: solid.append((r, a))
        r = b
    if r < 130: solid.append((r, 130.0))
    for a, b in solid:
        s.box(a, b, *FRAME, PLY)
    s.lbl(93, 1.2, "FACE 3 black", 2.9, "#fff")
    s.lbl(86, 9, "C channel", 2.8, "#777"); s.lbl(114, 9, "outer ch.", 2.8, "#777")
    s.lbl(124, 9, "ring", 2.8, "#777")
    s.lbl(93, 15.3, "FLOOR 3 black", 2.9, "#fff")
    s.lbl(93, 42.2, "CARRIER 3", 2.9, "#456")
    for r, t in ((60, "R60"), (79, "R79"), (93, "R93"), (102, "R102"), (110, "R110"),
                 (118, "R118"), (130, "R130")):
        s.tick(r, t)


def main():
    sh = Sheet(700, 680)
    sh.add('<rect x="0" y="0" width="700" height="44" fill="#15202b"/>')
    sh.text(26, 21, "TRON IDENTITY DISC — SECTIONS, REV 3", 10.5, "#fff", anchor="start",
            weight="700", ls="1.8")
    sh.text(26, 32, "radial cuts · z measured from the front of the face · 3.9 : 1", 4.3,
            "#8fb6d6", anchor="start")
    sh.add('<rect x="520" y="9" width="156" height="26" rx="3" fill="#b5179e"/>')
    sh.text(598, 20, "DRAFT", 11.0, "#fff", weight="700", ls="3")
    sh.text(598, 30, "not for cutting", 3.4, "#ffd9f3")

    # ---- A: down a covered bay's centre line
    a = Sec(sh, 60, 92, "SECTION A — down the buttons bay centre line (60°)",
            "the frame is cut away R60–R84 here; the cover closes the hand-hole end")
    common(a, [(60.0, 84.0)])
    a.box(61, 64, 16, 40, BLACK_AC, w=0.8)                       # cover, full frame height
    a.lbl(72, 18.5, "← COVER 3 flat", 3.0, INK, anchor="start", w="700")
    a.box(68.5, 70.3, 18, 38, RED, w=0.7, op=0.45)               # board on edge
    a.lbl(73, 24, "BOARD 38 × 20 on edge", 3.0, RED, anchor="start", w="700")
    a.box(60, 69, 26.5, 29.5, BLUE, w=0.6, op=0.5)               # switch, pointing in
    a.lbl(74, 29.5, "← switch tips reach R60, mid cover height", 2.9, BLUE, anchor="start", w="700")
    a.lbl(73, 37.5, "POCKET  R64–R84, open top and bottom", 3.1, "#8a7a52", anchor="start", w="700")

    # ---- B: through a wedge
    b = Sec(sh, 60, 338, "SECTION B — through a wedge (0°, 120° or 240°)",
            "solid wood the full depth; this is where every insert and the wire groove live")
    common(b, [])
    b.box(98, 106, 16, 26, BLUE, w=0.8, op=0.3)                  # front insert
    b.lbl(102, 30, "FRONT INSERT", 3.0, BLUE, w="700"); b.lbl(102, 33.3, "R102, z 16–26", 2.8, BLUE)
    b.box(76, 84, 30, 40, RED, w=0.8, op=0.3)                    # back insert
    b.lbl(82, 24, "BACK INSERT", 3.0, RED, w="700"); b.lbl(82, 27.3, "R80, z 30–40", 2.8, RED)
    b.box(70 - BIT / 2, 70 + BIT / 2, 34, 40, GREEN, w=0.8, op=0.45)   # wire groove
    b.lbl(64, 33, "WIRE GROOVE", 3.0, GREEN, w="700"); b.lbl(64, 36.3, "R70, 6 deep", 2.8, GREEN)
    b.lbl(118, 21, "SOLID — 24 mm", 3.4, "#8a7a52", w="700")

    ly = 536
    sh.text(26, ly, "WHAT THE SECTIONS SHOW THAT THE PLANS CANNOT", 4.8, INK, anchor="start",
            weight="700", ls="1.2")
    notes = [
        ("Front and back inserts can never meet.", GREEN,
         "R102 at z 16–26 against R80 at z 30–40: 22 mm apart radially and 4 mm apart in z."),
        ("The tightest z clearance in the build is 3 mm.", RED,
         "The cover insert runs radially at mid-height, z 25–31, and crosses R70 in plan. The wire",
         "groove is z 34–40. They miss by 3 mm, and only because the groove is cut from the back.",
         "Cut the groove deeper than 6 and they collide. Neither section plane shows this — it",
         "happens at the shoulders, bay x = ±28 and ±31."),
        ("The LED channels sit entirely above the frame.", GREY,
         "C channel R79–93 and outer channel R110–118 live in the upper frame at z 3–13. The pockets",
         "below reach R84 and R94. They share radius but never share z — the floor at z 13–16 divides",
         "them, which is also the light barrier."),
        ("The floor is the only thing bridging a pocket.", RED,
         "Section A shows it unsupported from R60 to R84. 3 mm acrylic, SF 2.9. See sheet 1."),
    ]
    y = ly + 9
    for head, col, *body in notes:
        sh.text(26, y, head, 3.8, col, anchor="start", weight="700"); y += 4.3
        for ln in body:
            sh.text(26, y, ln, 3.3, "#444", anchor="start"); y += 3.9
        y += 2.2
    sh.add('<rect x="0" y="670" width="700" height="10" fill="#15202b"/>')
    sh.text(26, 676.6, "build-plans/render/frame_section.py", 3.3, "#8fb6d6", anchor="start")
    open("frame-sections.svg", "w").write(sh.svg())
    print("wrote frame-sections.svg")


main()

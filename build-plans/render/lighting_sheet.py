#!/usr/bin/env python3
"""Where the two LED strips go — strips ON EDGE, which is the only way tape
follows a circle. Same constants as the v4 cut files."""
import math
from frame_render_v3 import Sheet

INK, GREY, BLUE = "#1b1b1b", "#8a9099", "#1f6fb4"
W, H = 1280, 790
PX, PY, PS = 372.0, 430.0, 1.80
R_HOLE, R_OUT = 60.0, 130.0
C_IN, C_OUT, C_GAP = 82.0, 88.0, 20.0
CH_C = (79.0, 93.0)
CH_OUT, RING_IN, FACE_OUT = 110.0, 118.0, 126.0
S_C, S_O = 93.0, 110.0                 # walls the strips stand on
LEAD = ((86.0, 352.0), (86.0, 8.0), (114.0, 352.0), (114.0, 8.0))


def p(r, phi):
    a = math.radians(phi)
    return (PX + r * PS * math.sin(a), PY - r * PS * math.cos(a))


def arcp(r, a0, a1, step=1.0):
    n = max(2, int(abs(a1 - a0) / step))
    return [p(r, a0 + (a1 - a0) * i / n) for i in range(n + 1)]


def path(pts, close=True):
    return "M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in pts) + (" Z" if close else "")


def band(sh, r0, r1, a0, a1, fill, op=1.0):
    sh.add(f'<path d="{path(arcp(r0,a0,a1) + list(reversed(arcp(r1,a0,a1))))}" '
           f'fill="{fill}" fill-opacity="{op}" stroke="none"/>')


def main():
    sh = Sheet(W, H)
    sh.add(f'<rect width="{W}" height="{H}" fill="#f4f5f6"/>')
    sh.text(52, 58, "WHERE THE LED STRIPS GO", 26, INK, anchor="start", weight="700", ls="1.0")
    sh.text(52, 82, "both strips stand ON EDGE against a circular wall — tape bends about its "
            "thickness, never sideways", 13.5, "#b5179e", anchor="start", weight="700")
    sh.text(52, 102, "a strip lying face-up cannot follow a circle at all. This is the corrected "
            "arrangement.", 12.5, "#5a6066", anchor="start")

    # ---------- plan ----------
    sh.text(PX, 146, "PLAN — channel layer, seen from the front", 15, INK, weight="700")
    band(sh, R_HOLE, CH_OUT, 0, 360, "#e3cda0")
    band(sh, *CH_C, C_GAP / 2, 360 - C_GAP / 2, "#ffffff")
    band(sh, RING_IN, R_OUT, 0, 360, "#f2f4f6")
    band(sh, C_IN, C_OUT, C_GAP / 2, 360 - C_GAP / 2, "#dfe6ea")
    for r in (R_HOLE, CH_C[0], CH_C[1], CH_OUT, RING_IN, R_OUT):
        sh.add(f'<circle cx="{PX}" cy="{PY}" r="{r*PS:.1f}" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    for r in (C_IN, C_OUT):
        sh.add(f'<path d="{path(arcp(r, C_GAP/2, 360-C_GAP/2), close=False)}" fill="none" '
               f'stroke="{INK}" stroke-width="0.9"/>')
    for r, a0, a1, n in ((S_C, C_GAP / 2, 360 - C_GAP / 2, 33), (S_O, 0, 358, 41)):
        sh.add(f'<path d="{path(arcp(r,a0,a1), close=False)}" fill="none" stroke={chr(34)}{BLUE}{chr(34)} '
               f'stroke-width="4.2" stroke-opacity="0.9"/>')
        for i in range(n):
            x, y = p(r, a0 + (a1 - a0) * (i + 0.5) / n)
            sh.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.2" fill="#6fc3df"/>')
    for i in range(44):                      # light arrows, showing which way each faces
        a = 8 + i * 8
        if C_GAP / 2 < a < 360 - C_GAP / 2:
            x0, y0 = p(S_C - 1.5, a); x1, y1 = p(C_OUT + 0.8, a)
            sh.add(f'<path d="M {x0:.1f},{y0:.1f} L {x1:.1f},{y1:.1f}" stroke="#6fc3df" stroke-width="1.3"/>')
        x0, y0 = p(S_O + 1.5, a); x1, y1 = p(RING_IN - 0.8, a)
        sh.add(f'<path d="M {x0:.1f},{y0:.1f} L {x1:.1f},{y1:.1f}" stroke="#6fc3df" stroke-width="1.3"/>')
    for r, a in LEAD:
        x, y = p(r, a)
        sh.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{4*PS:.1f}" fill="#2e7d4f" fill-opacity="0.4" '
               f'stroke="#2e7d4f" stroke-width="1.4"/>')
    sh.text(PX, PY + 5, "HAND HOLE", 12, GREY, weight="700")

    def lead(r, phi, tx, ty, lines, anchor="start"):
        x, y = p(r, phi)
        sh.add(f'<path d="M {x:.1f},{y:.1f} L {tx:.1f},{ty:.1f}" stroke="{INK}" stroke-width="1"/>')
        for i, ln in enumerate(lines):
            sh.text(tx + (6 if anchor == "start" else -6), ty + 4 + i * 14, ln,
                    13 if i == 0 else 11.5, INK if i == 0 else "#52585f", anchor=anchor,
                    weight="700" if i == 0 else "400")
    lead(S_C, 214, 208, 306, ["C STRIP — on the R93 wall", "facing IN at the white C bar",
                              "340°, 552 mm, 33 LEDs at 60/m"], "end")
    lead(S_O, 198, 208, 508, ["RING STRIP — on the R110 edge", "facing OUT at the white ring",
                              "360°, 691 mm, 41 LEDs at 60/m"], "end")
    lead(114, 10, 640, 186, ["Four Ø8 lead holes", "in the divider at 352° and 8°",
                             "either side of the C's solid gap"])

    # ---------- section ----------
    SX, SY, SS = 700.0, 320.0, 5.0
    def X(r): return SX + (r - 60) * SS
    def Z(z): return SY + z * SS
    sh.text(SX + 170, 146, "SECTION — strips standing on edge", 15, INK, weight="700")
    def box(r0, r1, z0, z1, f, s=INK):
        sh.add(f'<rect x="{X(r0):.1f}" y="{Z(z0):.1f}" width="{(r1-r0)*SS:.1f}" '
               f'height="{(z1-z0)*SS:.1f}" fill="{f}" stroke="{s}" stroke-width="0.8"/>')
    box(60, FACE_OUT, 0, 3, "#232629")                       # black face
    box(C_IN, C_OUT, 0, 9, "#f2f4f6")                        # white C bar, 9 tall
    box(RING_IN, 130, 3, 12, "#f2f4f6")                      # white ring, 9 thick
    box(60, CH_C[0], 3, 12, "#e3cda0"); box(CH_C[1], CH_OUT, 3, 12, "#e3cda0")
    box(60, 130, 12, 15, "#d8c49b")                          # divider
    box(S_C - 2, S_C, 3, 8, BLUE)                            # C strip, on edge
    box(S_O, S_O + 2, 3, 8, BLUE)                            # ring strip, on edge
    for x0, x1, zz in ((S_C - 2, C_OUT, 5.5), (S_O + 2, RING_IN, 5.5)):
        sh.add(f'<path d="M {X(x0):.1f},{Z(zz):.1f} L {X(x1):.1f},{Z(zz):.1f}" stroke="#6fc3df" '
               f'stroke-width="2.4" marker-end="url(#ar3)"/>')
    sh.define('<marker id="ar3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
              'orient="auto"><path d="M 0,1 L 10,5 L 0,9 z" fill="#6fc3df"/></marker>')
    for i, (r, t) in enumerate(((60, "R60"), (CH_C[0], "R79"), (C_IN, "R82"), (C_OUT, "R88"),
                                (S_C, "R93"), (CH_OUT, "R110"), (RING_IN, "R118"),
                                (FACE_OUT, "R126"), (130, "R130"))):
        sh.add(f'<path d="M {X(r):.1f},{Z(-1.5):.1f} V {Z(16.5 + (i % 2) * 3):.1f}" stroke="{GREY}" '
               f'stroke-width="0.4" stroke-dasharray="2,2"/>')
        sh.text(X(r), Z(19 + (i % 2) * 3), t, 10, GREY)
    for z, t in ((1.5, "face 3"), (7.5, "channel 9"), (13.5, "divider 3")):
        sh.text(X(130) + 14, Z(z) + 4, t, 11.5, "#52585f", anchor="start")
    sh.text(X(85), Z(-6), "white C bar, 9 tall", 12, INK, weight="700")
    sh.text(X(124), Z(-6), "white ring, 9 thick", 12, INK, weight="700")

    ny = 600
    sh.text(SX - 60, ny, "WHY ON EDGE", 15, INK, anchor="start", weight="700")
    for i, t in enumerate([
        "LED tape bends about its thickness, like a tape measure. It will not bend in its",
        "own plane. Lying face-up it cannot follow R93 or R110 at all — Brennan caught this.",
        "Standing on edge, the bend is through the thickness and the tape wraps happily.",
        "",
        "Use 5 mm bare tape. 10 mm will not stand up in a 9 mm channel — if that is what you",
        "have, cut the channel layer at 12 mm instead and everything else is unchanged.",
        "",
        "75 LEDs at 60/m. All-white is 4.5 A, well past the MT3608 — keep LED_MAX_MA near 1 A.",
        "Paint the channel walls and the divider floor white before the strips go in.",
    ]):
        sh.text(SX - 60, ny + 22 + i * 17, t, 12, "#434a52", anchor="start")
    sh.text(52, H - 22, "matches v4/4-channel-9mm-ply.svg  ·  build-plans/render/lighting_sheet.py",
            10.5, GREY, anchor="start")
    open("v4/PREVIEW-lighting.svg", "w").write(sh.svg())
    print("wrote v4/PREVIEW-lighting.svg")


main()

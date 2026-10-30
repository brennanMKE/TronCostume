#!/usr/bin/env python3
"""Where the two LED strips go. Same constants as the v4 cut files."""
import math
from frame_render_v3 import Sheet

INK, GREY = "#1b1b1b", "#8a9099"
W, H = 1240, 760
PX, PY, PS = 372.0, 424.0, 1.82        # plan view
R_HOLE, R_OUT = 60.0, 130.0
C_IN, C_OUT, C_GAP = 82.0, 88.0, 20.0
RING_IN = 118.0
CH_C, CH_O = (79.0, 91.0), (117.0, 127.0)
STRIP_C, STRIP_O = 85.0, 122.0
LEAD = ((85.0, 352.0), (85.0, 8.0), (122.0, 352.0), (122.0, 8.0))


def p(r, phi, cx=PX, cy=PY, s=PS):
    a = math.radians(phi)
    return (cx + r * s * math.sin(a), cy - r * s * math.cos(a))


def arcp(r, a0, a1, step=1.0, **k):
    n = max(2, int(abs(a1 - a0) / step))
    return [p(r, a0 + (a1 - a0) * i / n, **k) for i in range(n + 1)]


def path(pts, close=True):
    return "M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in pts) + (" Z" if close else "")


def band(sh, r0, r1, a0, a1, fill, op=1.0, stroke="none"):
    sh.add(f'<path d="{path(arcp(r0,a0,a1) + list(reversed(arcp(r1,a0,a1))))}" '
           f'fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="0.8"/>')


def main():
    sh = Sheet(W, H)
    sh.add(f'<rect width="{W}" height="{H}" fill="#f4f5f6"/>')
    sh.text(52, 58, "WHERE THE LED STRIPS GO", 26, INK, anchor="start", weight="700", ls="1.0")
    sh.text(52, 82, "both strips lie FLAT on the divider, LEDs facing UP at the white acrylic "
            "7 mm above them", 13.5, "#5a6066", anchor="start")

    # ---------- plan view ----------
    sh.text(PX, 128, "PLAN — channel layer, seen from the front", 15, INK, weight="700")
    band(sh, R_HOLE, R_OUT, 0, 360, "#e3cda0")                       # ply
    band(sh, *CH_C, C_GAP / 2, 360 - C_GAP / 2, "#ffffff")           # C channel void
    band(sh, *CH_O, 0, 360, "#ffffff")                               # outer channel void
    for r0, r1, a0, a1 in ((CH_C[0], CH_C[1], C_GAP / 2, 360 - C_GAP / 2), (CH_O[0], CH_O[1], 0, 360)):
        sh.add(f'<path d="{path(arcp(r0,a0,a1), close=False)}" fill="none" stroke="{INK}" stroke-width="1"/>')
        sh.add(f'<path d="{path(arcp(r1,a0,a1), close=False)}" fill="none" stroke="{INK}" stroke-width="1"/>')
    sh.add(f'<circle cx="{PX}" cy="{PY}" r="{R_OUT*PS:.1f}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    sh.add(f'<circle cx="{PX}" cy="{PY}" r="{R_HOLE*PS:.1f}" fill="#f4f5f6" stroke="{INK}" stroke-width="1.2"/>')
    # the strips themselves, drawn as LEDs
    for r, a0, a1, n in ((STRIP_C, C_GAP / 2, 360 - C_GAP / 2, 30), (STRIP_O, 0, 358, 46)):
        sh.add(f'<path d="{path(arcp(r,a0,a1), close=False)}" fill="none" stroke="#1f6fb4" '
               f'stroke-width="{5*PS:.1f}" stroke-opacity="0.30" stroke-linecap="butt"/>')
        for i in range(n):
            x, y = p(r, a0 + (a1 - a0) * (i + 0.5) / n)
            sh.add(f'<rect x="{x-2.6:.1f}" y="{y-2.6:.1f}" width="5.2" height="5.2" rx="1" '
                   f'fill="#6fc3df" stroke="#1f6fb4" stroke-width="0.7"/>')
    for r, a in LEAD:
        x, y = p(r, a)
        sh.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{4*PS:.1f}" fill="#2e7d4f" fill-opacity="0.35" '
               f'stroke="#2e7d4f" stroke-width="1.4"/>')
    x, y = p(0, 0); sh.text(x, PY - R_HOLE * PS - 10, "C gap, 12 o'clock — solid wood", 11, "#6b5a36", weight="700")
    sh.text(PX, PY + 4, "HAND HOLE", 12, GREY, weight="700")

    def lead(r, phi, tx, ty, lines, anchor="start"):
        x, y = p(r, phi)
        sh.add(f'<path d="M {x:.1f},{y:.1f} L {tx:.1f},{ty:.1f}" stroke="{INK}" stroke-width="1"/>')
        for i, ln in enumerate(lines):
            sh.text(tx + (6 if anchor == "start" else -6), ty + 4 + i * 14, ln,
                    13 if i == 0 else 11.5, INK if i == 0 else "#52585f", anchor=anchor,
                    weight="700" if i == 0 else "400")
    lead(STRIP_C, 212, 178, 300, ["C STRIP", "on R85, 340°, 504 mm", "30 LEDs at 60/m"], "end")
    lead(STRIP_O, 196, 178, 486, ["RING STRIP", "on R122, full circle, 767 mm", "46 LEDs at 60/m"], "end")
    lead(122, 10, 626, 182, ["Four Ø8 lead holes", "in the divider, R85 and R122", "at 352° and 8°"])

    # ---------- section ----------
    SX, SY, SS = 690.0, 304.0, 4.9
    def X(r): return SX + (r - 60) * SS
    def Z(z): return SY + z * SS
    sh.text(SX + 170, 128, "SECTION — top three layers", 15, INK, weight="700")
    sh.text(SX + 170, 146, "radial cut, 4.3 : 1", 11.5, "#5a6066")
    def box(r0, r1, z0, z1, f, s=INK):
        sh.add(f'<rect x="{X(r0):.1f}" y="{Z(z0):.1f}" width="{(r1-r0)*SS:.1f}" '
               f'height="{(z1-z0)*SS:.1f}" fill="{f}" stroke="{s}" stroke-width="0.8"/>')
    box(60, RING_IN, 0, 3, "#232629")                       # black face
    box(C_IN, C_OUT, 0, 3, "#f2f4f6")                       # white C inset
    box(RING_IN, 130, 0, 3, "#f2f4f6")                      # white ring
    box(60, CH_C[0], 3, 12, "#e3cda0"); box(CH_C[1], CH_O[0], 3, 12, "#e3cda0")
    box(CH_O[1], 130, 3, 12, "#e3cda0")
    box(60, 130, 12, 15, "#d8c49b")                         # divider
    for r in (STRIP_C, STRIP_O):                            # strips, flat, facing up
        box(r - 2.5, r + 2.5, 10, 12, "#1f6fb4")
        for dz in range(3):
            pass
        sh.add(f'<path d="M {X(r):.1f},{Z(10):.1f} L {X(r):.1f},{Z(4.2):.1f}" stroke="#6fc3df" '
               f'stroke-width="3" marker-end="url(#up)"/>')
    sh.define('<marker id="up" viewBox="0 0 10 10" refX="5" refY="2" markerWidth="6" markerHeight="6" '
              'orient="auto"><path d="M 5,0 L 10,8 L 0,8 z" fill="#6fc3df"/></marker>')
    for i, (r, t) in enumerate(((60, "R60"), (CH_C[0], "R79"), (C_IN, "R82"), (C_OUT, "R88"),
                                (CH_C[1], "R91"), (CH_O[0], "R117"), (RING_IN, "R118"),
                                (CH_O[1], "R127"), (130, "R130"))):
        sh.add(f'<path d="M {X(r):.1f},{Z(-1.5):.1f} V {Z(16.5 + (i % 2) * 3):.1f}" stroke="{GREY}" '
               f'stroke-width="0.4" stroke-dasharray="2,2"/>')
        sh.text(X(r), Z(19.0 + (i % 2) * 3), t, 10, GREY)
    for z, t in ((1.5, "top plate 3"), (7.5, "channel layer 9"), (13.5, "divider 3")):
        sh.text(X(130) + 14, Z(z) + 4, t, 11.5, "#52585f", anchor="start")
    sh.text(X(85), Z(-6), "white C", 12, INK, weight="700")
    sh.text(X(124), Z(-6), "white ring", 12, INK, weight="700")
    sh.text(X(95), Z(30), "7 mm of air between the LEDs and the white — enough to blur the dots",
            11.5, "#52585f")

    # ---------- notes ----------
    ny = 582
    sh.text(SX - 50, ny, "WIRING AND POWER", 15, INK, anchor="start", weight="700")
    for i, t in enumerate([
        "One data line, two segments: GPIO 4 → 330 Ω → C strip in at 350°, round to 10°,",
        "down a divider hole into the electronics bay, back up into the outer channel.",
        "5 V and GND to the start of each strip.",
        "",
        "76 LEDs at 60/m, or 153 at 120/m.  All-white worst case is 4.6 A, far beyond the",
        "MT3608 — keep LED_MAX_MA set so you stay near 1 A. Paint the channels white first.",
    ]):
        sh.text(SX - 50, ny + 22 + i * 17, t, 12, "#434a52", anchor="start")
    sh.text(52, H - 24, "matches v4/4-channel-9mm-ply.svg and v4/5-divider-3mm-ply.svg  ·  "
            "build-plans/render/lighting_sheet.py", 10.5, GREY, anchor="start")
    open("v4/PREVIEW-lighting.svg", "w").write(sh.svg())
    print("wrote v4/PREVIEW-lighting.svg")


main()

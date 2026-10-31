#!/usr/bin/env python3
"""One picture: the whole 42 mm stack, with the LEDs and the components in it.

The LEDs live in the top 12 mm. The components live in the 24 mm below the
divider. They are at different depths AND different radii, so they never meet.
"""
import math
from frame_render_v3 import Sheet

INK, GREY, BLUE, RED, GREEN = "#1b1b1b", "#8a9099", "#1f6fb4", "#b03a2e", "#2e7d4f"
W, H = 1240, 900
SX, SY, S = 150.0, 240.0, 7.6          # px per mm
PLY, PLY_D, BLACK, WHITE, ACR = "#e3cda0", "#c9ad7c", "#232629", "#f2f4f6", "#bfe3f2"


def X(r): return SX + (r - 60) * S
def Z(z): return SY + z * S


def box(sh, r0, r1, z0, z1, f, lbl=None, tc="#fff", s=INK, sw=0.9, fs=11):
    sh.add(f'<rect x="{X(r0):.1f}" y="{Z(z0):.1f}" width="{(r1-r0)*S:.1f}" '
           f'height="{(z1-z0)*S:.1f}" fill="{f}" stroke="{s}" stroke-width="{sw}"/>')
    if lbl:
        sh.text((X(r0)+X(r1))/2, (Z(z0)+Z(z1))/2 + fs*0.35, lbl, fs, tc, weight="700")


def main():
    sh = Sheet(W, H)
    sh.add(f'<rect width="{W}" height="{H}" fill="#f4f5f6"/>')
    sh.text(52, 56, "WHERE EVERYTHING LIVES", 27, INK, anchor="start", weight="700", ls="1.0")
    sh.text(52, 80, "one radial slice through the disc, at the battery bay · 42 mm total · "
            "scale 7.6 : 1", 13.5, "#5a6066", anchor="start")
    sh.text(52, 100, "LEDs live in the top 12 mm. Components live in the 24 mm below the divider. "
            "Different depth AND different radius — they never meet.", 13, "#b5179e",
            anchor="start", weight="700")

    # ---- the five layers
    box(sh, 60, 126, 0, 3, BLACK, None)                       # 1
    box(sh, 82, 88, 0, 9, WHITE, None, s=INK)                               # white C bar
    box(sh, 118, 130, 3, 12, WHITE, None, s=INK)                            # white ring 9
    box(sh, 60, 79, 3, 12, PLY, None); box(sh, 93, 110, 3, 12, PLY, None)   # 2 channel layer
    box(sh, 60, 130, 12, 15, PLY_D, "DIVIDER  3 mm — the part that makes it a box", INK, fs=11)
    box(sh, 60, 72, 15, 39, PLY, None)                                      # 4 frame: inner rim
    box(sh, 110, 130, 15, 39, PLY, None)                                    # 4 frame: outer rim
    box(sh, 60, 130, 39, 42, ACR, "CARRIER / BACK  3 mm acrylic — everything bolts to this", INK, fs=11)

    # ---- the LEDs, on edge
    box(sh, 91, 93, 3, 8, BLUE, None, sw=0.7)
    box(sh, 110, 112, 3, 8, BLUE, None, sw=0.7)
    sh.define('<marker id="lr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
              'orient="auto"><path d="M 0,1 L 10,5 L 0,9 z" fill="#6fc3df"/></marker>')
    for a, b in ((91, 88.4), (112, 117.4)):
        sh.add(f'<path d="M {X(a):.1f},{Z(5.5):.1f} L {X(b):.1f},{Z(5.5):.1f}" stroke="#6fc3df" '
               f'stroke-width="2.6" marker-end="url(#lr)"/>')

    # ---- the components, standing on the carrier
    box(sh, 76, 97, 18, 39, "#8e44ad", "18650 in its holder — 21 mm tall", "#fff", fs=11)
    sh.add(f'<path d="M {X(76):.1f},{Z(15):.1f} H {X(97):.1f}" stroke="{RED}" stroke-width="1.2" '
           f'stroke-dasharray="4,3"/>')
    sh.text(X(86.5), Z(16.6), "3 mm clear", 9.5, RED, weight="700")

    # ---- radius ticks
    for i, (r, t) in enumerate(((60, "R60"), (72, "R72"), (79, "R79"), (88, "R88"), (93, "R93"),
                                (110, "R110"), (118, "R118"), (126, "R126"), (130, "R130"))):
        sh.add(f'<path d="M {X(r):.1f},{Z(-2):.1f} V {Z(43.5 + (i%2)*3.2):.1f}" stroke={chr(34)}{GREY}{chr(34)} '
               f'stroke-width="0.4" stroke-dasharray="2,2"/>')
        sh.text(X(r), Z(46.5 + (i%2)*3.2), t, 10.5, GREY)
    sh.text(X(70), Z(1.9), "BLACK FACE 3 mm", 10.5, "#fff", weight="700")
    sh.text(X(66), Z(-4.5), "hand hole wall", 11, GREY)
    sh.text(X(95), Z(-4.5), "LED CHANNELS", 12.5, BLUE, weight="700")
    sh.text(X(120), Z(-4.5), "white ring", 11, GREY)

    # ---- the thickness ladder
    LX = X(130) + 70
    sh.text(LX, Z(-4.5), "THICKNESS", 13, INK, anchor="start", weight="700")
    rows = ((0, 3, "face", "3", BLACK), (3, 12, "channel layer — the LEDs", "9", PLY),
            (12, 15, "divider", "3", PLY_D), (15, 39, "frame — the components", "24", PLY),
            (39, 42, "carrier / back", "3", ACR))
    for z0, z1, nm, mm, col in rows:
        sh.add(f'<rect x="{LX}" y="{Z(z0):.1f}" width="26" height="{(z1-z0)*S:.1f}" fill="{col}" '
               f'stroke="{INK}" stroke-width="0.8"/>')
        sh.text(LX + 36, (Z(z0)+Z(z1))/2 + 4, f"{mm} mm   {nm}", 12.5, "#333", anchor="start")
    sh.add(f'<path d="M {LX-20:.1f},{Z(0):.1f} V {Z(42):.1f}" stroke="{INK}" stroke-width="1.4" '
           f'marker-start="url(#t2)" marker-end="url(#t2)"/>')
    sh.define(f'<marker id="t2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
              f'orient="auto-start-reverse"><path d="M 0,1 L 10,5 L 0,9 z" fill="{INK}"/></marker>')
    sh.text(LX - 28, Z(21) + 5, "42 mm", 17, INK, anchor="end", weight="700")

    # ---- notes
    ny = Z(58)
    sh.text(52, ny, "SO, TO ANSWER BOTH QUESTIONS", 15, INK, anchor="start", weight="700")
    for i, t in enumerate([
        "The LED strips never share space with the electronics. The strips stand on edge in the",
        "9 mm channel layer, between R79 and R110, in the top 12 mm of the disc. The boards, the",
        "battery and the button board all sit in the 24 mm frame below the divider, between R72",
        "and R110. The divider is the floor of one and the ceiling of the other.",
        "",
        "Total 42 mm. The 18650 holder is what sets it: 21 mm tall, in a 24 mm bay, 3 mm clear.",
        "Drop to a bare tabbed cell and an 18 mm frame and the disc becomes 36 mm.",
    ]):
        sh.text(52, ny + 24 + i * 18, t, 12.5, "#434a52", anchor="start")
    sh.text(52, H - 22, "build-plans/render/stack_section.py  ·  same constants as the v4 cut files",
            10.5, GREY, anchor="start")
    open("v4/PREVIEW-stack.svg", "w").write(sh.svg())
    print("wrote v4/PREVIEW-stack.svg")


main()

#!/usr/bin/env python3
"""The lower frame with everything in it — the view that answers
"how do I seat all the components".  Geometry from docs/disc-build.md.
"""
import math
import disc_exploded as D
from frame_render_v3 import Sheet

S, K = 2.15, 0.46
CX, CY = 560.0, 430.0
D.S, D.K, D.CX = S, K, CX
R_HOLE, R_RIM, R_OUT = 60.0, 110.0, 130.0
BAYS = ((60.0, "BUTTONS", 60.0), (180.0, "BATTERY", 72.0), (300.0, "ELECTRONICS", 60.0))


def V(px, py): return (CX + (px - CX) * S, CY - (CY - py) * K * S)
def pol(r, phi):
    a = math.radians(phi); return (CX + r * math.sin(a), CY - r * math.cos(a))
def bp(A, x, y):
    a = math.radians(A)
    return (CX + y * math.sin(a) + x * math.cos(a), CY - y * math.cos(a) + x * math.sin(a))
def quad(A, x0, x1, y0, y1):
    return [bp(A, x0, y0), bp(A, x0, y1), bp(A, x1, y1), bp(A, x1, y0)]
def pathof(pts): return "M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z"


def main():
    sh = Sheet(1180, 820)
    sh.define('<radialGradient id="bg" cx="44%" cy="36%" r="76%">'
              '<stop offset="55%" stop-color="#f3f4f5"/><stop offset="100%" stop-color="#d6d9dd"/></radialGradient>')
    sh.add('<rect width="1180" height="820" fill="url(#bg)"/>')
    sh.text(56, 58, "LOWER FRAME — HOW THE COMPONENTS SEAT", 23, "#1b1b1b", anchor="start", weight="700", ls="1.0")
    sh.text(56, 80, "24 mm plywood · three 24 mm bridges · buttons and electronics open to the hand hole · v4",
            12.5, "#5a5f66", anchor="start")

    drop = 18 * 0.86 * S
    cuts = [D.circ(CY, R_HOLE)] + [D.bay_cut(CY, A, ri) for A, _, ri in BAYS]
    tf = f'translate({CX},{CY}) scale({S},{K*S}) translate({-CX},{-CY})'
    sh.define(f'<mask id="lf"><g transform="{tf}"><path d="{D.circ(CY,R_OUT)}" fill="#fff"/>'
              + "".join(f'<path d="{d}" fill="#000"/>' for d in cuts) + '</g></mask>')
    D.ring_wall(sh, CY, R_HOLE, drop, D.WOOD_D, False)
    for A, _, ri in BAYS:                      # bay side + outer walls
        for a0, a1, outw in ((A-60+D.bay_span(R_RIM), A+60-D.bay_span(R_RIM), False),):
            D.ring_wall(sh, CY, R_RIM, drop, D.WOOD_D, outw, a0, a1)
    D.ring_wall(sh, CY, R_OUT, drop, D.WOOD_D, True)
    sh.add(f'<g mask="url(#lf)"><g transform="{tf}">'
           f'<path d="{D.circ(CY,R_OUT)}" fill="#ddc292"/></g></g>')
    sh.add(f'<g mask="url(#lf)" fill="none" stroke="#000" stroke-opacity="0.32" stroke-width="0.9">'
           f'<g transform="{tf}">')
    for d in cuts + [D.circ(CY, R_OUT)]:
        sh.add(f'<path d="{d}"/>')
    sh.add('</g></g>')

    def part(A, x0, x1, y0, y1, fill, stroke, op=0.95):
        sh.add(f'<path d="{pathof([V(*p) for p in quad(A,x0,x1,y0,y1)])}" fill="{fill}" '
               f'fill-opacity="{op}" stroke="{stroke}" stroke-width="1.0"/>')

    part(300, -32, -14, 73, 95.5, "#b03a2e", "#6d1f16")          # ESP32-C3
    part(300, -10, 7, 73, 101, "#b03a2e", "#6d1f16")             # TP4056
    part(300, 12, 48, 76, 93, "#7a5c2e", "#4a3718")              # MT3608
    for x in (-23, -1.5):                                        # USB-C mouths, at the hand hole
        part(300, x - 4.5, x + 4.5, 66, 73, "#e8e2d2", "#555")
    part(60, -41, 41, 71.1, 72.9, "#1f6fb4", "#123f66")          # protoboard on edge
    for bx in (-27, -9, 9, 27):
        part(60, bx - 3, bx + 3, 62, 71, "#1f6fb4", "#123f66")
    part(180, -38.5, 38.5, 76, 97, "#6b5a36", "#3b3119")         # 18650 holder

    sh.define('<marker id="d2" viewBox="0 0 6 6" refX="3" refY="3" markerWidth="5" markerHeight="5">'
              '<circle cx="3" cy="3" r="2.4" fill="#1b1b1b"/></marker>')
    def lead(px, py, tx, ty, lines, anchor="start"):
        x, y = V(px, py)
        sh.add(f'<path d="M {x:.1f},{y:.1f} L {tx:.1f},{ty:.1f}" stroke="#1b1b1b" '
               f'stroke-width="1.0" marker-start="url(#d2)"/>')
        for i, ln in enumerate(lines):
            sh.text(tx + (6 if anchor == "start" else -6), ty + 4 + i * 13, ln,
                    12.5 if i == 0 else 11, "#1b1b1b" if i == 0 else "#52585f",
                    anchor=anchor, weight="700" if i == 0 else "400")

    lead(*bp(300, 0, 97), 292, 180, ["ALL THREE BOARDS",
         "mount to the 3 mm acrylic back.", "Build and test it on the bench,",
         "then ten screws and it is in."], anchor="end")
    lead(*bp(300, -31, 62), 292, 322, ["Both USB-C at the hand hole",
         "this bay runs straight into the", "hand hole — no wall, no cover"], anchor="end")
    lead(*bp(60, 0, 71), 944, 180, ["PROTOBOARD, on edge",
         "four 6×6 switches pointing", "at the hand hole"])
    lead(*bp(60, 27, 64), 944, 292, ["Switches at 18 mm pitch",
         "reach straight into the hand hole"])
    lead(*pol(90, 0), 944, 382, ["Ø8 through the 0° bridge",
         "the five button wires cross here"])
    lead(*bp(180, 0, 86), 620, 676, ["18650 holder",
         "inner rim stays solid here —", "this is where your hand grips"])
    lead(*pol(120, 120), 944, 486, ["Bridge, 24 mm wide",
         "back fasteners at R70 and R102,", "plus four at R122 in the rim"])
    sh.text(56, 776, "matches v4/7-router-template-acrylic.svg  ·  build-plans/render/carrier_layout.py",
            10, "#8a9099", anchor="start")
    open("v4/PREVIEW-bays.svg", "w").write(sh.svg())
    print("wrote v4/PREVIEW-bays.svg")


main()

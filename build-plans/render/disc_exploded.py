#!/usr/bin/env python3
"""Exploded view of the disc exactly as docs/disc-build.md specifies it.

Not a new design. The five-layer laminated box from that document's
cross-section, with the three-bridge lower frame and the components where it
puts them.
"""
import math
from frame_render_v3 import Sheet

K, S = 0.42, 1.30
CX = 560.0
GAP = 158.0
TOP = 232.0
WOOD, WOOD_D = (0xdd, 0xc2, 0x92), (0x8c, 0x72, 0x49)
BLACK, BLACKD = "#232629", "#121416"
WHITE_AC, WHITE_D = "#eef0f2", "#b9bfc5"
ACRYL, ACRYLD = "#9fd3e8", "#5f93a8"
LIGHT = (-0.55, 0.835)

BRIDGES = (0.0, 120.0, 240.0)
BAYS = ((60.0, "BUTTONS", 90.0), (180.0, "BATTERY", 90.0), (300.0, "ELECTRONICS", 100.0))
BR_HALF = 12.0                       # bridges are 24 wide
R_HOLE, R_OUT = 60.0, 130.0
R_RIM = 110.0                        # outer rim inner edge
COV_T, COV_Y = 6.0, 61.0             # cover 6 thick, front face 1 mm behind the hole


def V(cy, px, py):
    return (CX + (px - CX) * S, cy - (cy - py) * K * S)


def pol(cy, r, phi):
    a = math.radians(phi)
    return (CX + r * math.sin(a), cy - r * math.cos(a))


def bay_pt(cy, A, x, y):
    a = math.radians(A)
    return (CX + y * math.sin(a) + x * math.cos(a), cy - y * math.cos(a) + x * math.sin(a))


def shade(base, nx, ny, amb=0.42, k=0.6):
    m = math.hypot(nx, ny) or 1.0
    lam = max(0.0, (nx / m) * LIGHT[0] + (ny / m) * LIGHT[1])
    f = amb + k * lam
    return "#%02x%02x%02x" % tuple(min(255, int(c * f)) for c in base)


def circ(cy, r):
    return (f'M {CX-r:.3f},{cy:.3f} a {r:.3f},{r:.3f} 0 1,0 {2*r:.3f},0 '
            f'a {r:.3f},{r:.3f} 0 1,0 {-2*r:.3f},0 Z')


def pathof(pts):
    return "M " + " L ".join(f"{x:.3f},{y:.3f}" for x, y in pts) + " Z"


def arcpts(cy, r, a0, a1, step=1.0):
    n = max(2, int(abs(a1 - a0) / step))
    return [pol(cy, r, a0 + (a1 - a0) * i / n) for i in range(n + 1)]


def ring_wall(sh, cy, r, drop, base, outward, a0=0.0, a1=360.0, step=2.0):
    n = max(2, int(abs(a1 - a0) / step))
    for i in range(n):
        p0 = pol(cy, r, a0 + (a1 - a0) * i / n)
        p1 = pol(cy, r, a0 + (a1 - a0) * (i + 1) / n)
        mid = math.radians(a0 + (a1 - a0) * (i + 0.5) / n)
        s = 1.0 if outward else -1.0
        nx, ny = s * math.sin(mid), s * math.cos(mid)
        if ny >= 0:
            continue
        a, b = V(cy, *p0), V(cy, *p1)
        col = shade(base, nx, ny)
        sh.add(f'<path d="M {a[0]:.2f},{a[1]:.2f} L {b[0]:.2f},{b[1]:.2f} '
               f'L {b[0]:.2f},{b[1]+drop:.2f} L {a[0]:.2f},{a[1]+drop:.2f} Z" '
               f'fill="{col}" stroke="{col}" stroke-width="0.4"/>')


def layer(sh, uid, cy, thick, base, fill, keep, cut, label, sub, inner=R_HOLE, outer=R_OUT):
    drop = thick * 0.86 * S
    tf = f'translate({CX},{cy}) scale({S},{K*S}) translate({-CX},{-cy})'
    sh.define(f'<mask id="k{uid}"><g transform="{tf}">'
              + "".join(f'<path d="{d}" fill="#fff"/>' for d in keep)
              + "".join(f'<path d="{d}" fill="#000"/>' for d in cut) + '</g></mask>')
    if inner:
        ring_wall(sh, cy, inner, drop, base, outward=False)
    ring_wall(sh, cy, outer, drop, base, outward=True)
    sh.add(f'<g mask="url(#k{uid})"><g transform="{tf}">'
           f'<path d="{circ(cy, outer)}" fill="{fill}"/></g></g>')
    sh.add(f'<g mask="url(#k{uid})" fill="none" stroke="#000" stroke-opacity="0.35" '
           f'stroke-width="0.9"><g transform="{tf}">')
    for d in keep + cut:
        sh.add(f'<path d="{d}"/>')
    sh.add('</g></g>')
    lx = CX + outer * S + 46
    sh.add(f'<path d="M {CX + outer*S*0.72:.1f},{cy - outer*S*K*0.40:.1f} L {lx-8:.1f},{cy-6:.1f}" '
           f'stroke="#1b1b1b" stroke-width="0.9"/>')
    sh.text(lx, cy - 4, label, 13.5, "#1b1b1b", anchor="start", weight="700")
    for i, ln in enumerate(sub):
        sh.text(lx, cy + 11 + i * 12, ln, 10.5, "#555b62", anchor="start")


def bay_span(r):
    """angular half-gap taken by a bridge at this radius"""
    return math.degrees(math.asin(min(1.0, BR_HALF / r)))


def bay_cut(cy, A, r_in=None):
    """open sector between two bridges, from r_in out to the outer rim"""
    r_in = R_HOLE if r_in is None else r_in
    a0, a1 = A - 60 + bay_span(r_in), A + 60 - bay_span(r_in)
    pts = arcpts(cy, r_in, a0, a1)
    o0, o1 = A - 60 + bay_span(R_RIM), A + 60 - bay_span(R_RIM)
    pts += list(reversed(arcpts(cy, R_RIM, o0, o1)))
    return pathof(pts)


def main():
    sh = Sheet(1180, 1080)
    sh.define('<radialGradient id="bg" cx="42%" cy="34%" r="78%">'
              '<stop offset="55%" stop-color="#f3f4f5"/><stop offset="100%" stop-color="#d6d9dd"/></radialGradient>')
    sh.add('<rect width="1180" height="1080" fill="url(#bg)"/>')
    sh.text(56, 62, "TRON IDENTITY DISC — EXPLODED", 25, "#1b1b1b", anchor="start", weight="700", ls="1.2")
    sh.text(56, 86, "exactly as docs/disc-build.md specifies it · 42 mm total · Ø260",
            12.5, "#5a5f66", anchor="start")
    sh.text(56, 104, "three-bridge lower frame · the divider is what ties it into a box",
            12.5, "#5a5f66", anchor="start")

    cy = TOP
    # 1 — face
    cslot = pathof(arcpts(cy, 88, 10, 350) + list(reversed(arcpts(cy, 82, 10, 350))))
    layer(sh, "face", cy, 6, (0x2a, 0x2e, 0x32), BLACK,
          [circ(cy, 126)], [circ(cy, R_HOLE), cslot],
          "1 · FACE — black acrylic 6 mm",
          ["OD 252, hole Ø120", "C window R82–88, one 20° gap at 12 o'clock"], outer=126)

    # 2 — upper frame + white ring
    cy += GAP
    cch = pathof(arcpts(cy, 94, 10, 350) + list(reversed(arcpts(cy, 80, 10, 350))))
    och = pathof(arcpts(cy, 118, 0, 360) + list(reversed(arcpts(cy, 110, 0, 360))))
    layer(sh, "up", cy, 9, WOOD_D, "#e3cda0",
          [circ(cy, 118)], [circ(cy, R_HOLE), cch, och],
          "2 · UPPER FRAME — plywood 9 mm",
          ["C channel R80–94 · middle band R94–110 · outer channel R110–118",
           "both LED strips stand on edge against a channel wall"], outer=118)
    ring_wall(sh, cy, 130, 9 * 0.86 * S, (0xc9, 0xcf, 0xd4), True)
    tf = f'translate({CX},{cy}) scale({S},{K*S}) translate({-CX},{-cy})'
    sh.define(f'<mask id="kring"><g transform="{tf}"><path d="{circ(cy,130)}" fill="#fff"/>'
              f'<path d="{circ(cy,118)}" fill="#000"/></g></mask>')
    sh.add(f'<g mask="url(#kring)"><g transform="{tf}">'
           f'<path d="{circ(cy,130)}" fill="{WHITE_AC}"/></g></g>')
    sh.text(CX - 118 * S - 46, cy, "white ring 9 mm", 10.5, "#5a5f66", anchor="end", weight="700")
    sh.text(CX - 118 * S - 46, cy + 12, "R118–130, lit from inside", 10, "#7a8088", anchor="end")

    # 3 — divider: the part that makes it a box
    cy += GAP
    layer(sh, "div", cy, 3, WOOD_D, "#e8d4ab",
          [circ(cy, 130)], [circ(cy, R_HOLE)],
          "3 · DIVIDER — plywood 3 mm",
          ["full annulus Ø260/Ø120, only small wire holes",
           "THIS is the sandwich: it ties upper frame, lower frame and ring into one box"])

    # 4 — lower frame: three bridges, three open bays
    cy += GAP
    cuts = [circ(cy, R_HOLE)] + [bay_cut(cy, A) for A, _, _ in BAYS]
    layer(sh, "low", cy, 18, WOOD_D, "#ddc292",
          [circ(cy, 130)], cuts,
          "4 · LOWER FRAME — plywood 18 mm",
          ["three 24 mm-wide bridges at 0° / 120° / 240°, R60 out to the rim",
           "three open bays between them — this is where everything lives",
           "components shown in place; see disc-bays.png for how they seat"])
    # components, sitting in the bays
    def part(A, x0, x1, y0, y1, fill, stroke, lbl=None, tcol="#1b1b1b"):
        pts = [bay_pt(cy, A, x0, y0), bay_pt(cy, A, x0, y1), bay_pt(cy, A, x1, y1), bay_pt(cy, A, x1, y0)]
        sh.add(f'<path d="{pathof([V(cy,*p) for p in pts])}" fill="{fill}" fill-opacity="0.92" '
               f'stroke="{stroke}" stroke-width="0.8"/>')
        if lbl:
            mx, my = V(cy, *bay_pt(cy, A, (x0 + x1) / 2, (y0 + y1) / 2))
            sh.text(mx, my + 3, lbl, 8.2, tcol, weight="700")
    # electronics bay 300: 3 mm acrylic carrier, then the three boards on it
    part(300, -46, 46, 66, 104, ACRYL, ACRYLD)

    part(300, -40, -22, 67, 89.5, "#b03a2e", "#7d2318", None)
    part(300, -18, -1, 67, 95, "#b03a2e", "#7d2318", None)
    part(300, 4, 40, 72, 89, "#7a5c2e", "#4e3a18", None)
    # buttons bay 60: vertical protoboard + four switches
    part(60, -45, 45, 70, 73, "#1f6fb4", "#14466f", None)
    for bx in (-27, -9, 9, 27):
        part(60, bx - 2.5, bx + 2.5, 61, 70, "#1f6fb4", "#14466f")
    # battery bay 180: cell as a chord in a wood cradle
    part(180, -38, 38, 66, 90, "#6b5a36", "#3f3420", None)
    part(180, -33.5, 33.5, 68, 86.5, "#8e44ad", "#5b2c6f", None)
    # the three covers, standing in the hand-hole wall
    for A, nm, L in BAYS:
        part(A, -L / 2, L / 2, COV_Y, COV_Y + COV_T, BLACK, "#000")


    # 5 — back cover
    cy += GAP
    mag = pathof([V(cy, *bay_pt(cy, 180, x, y)) for x, y in
                  ((-32.5, 104), (-32.5, 119), (32.5, 119), (32.5, 104))])
    magplan = pathof([bay_pt(cy, 180, x, y) for x, y in
                      ((-32.5, 104), (-32.5, 119), (32.5, 119), (32.5, 104))])
    layer(sh, "back", cy, 6, (0x2a, 0x2e, 0x32), BLACK,
          [circ(cy, 130)], [circ(cy, R_HOLE), magplan],
          "5 · BACK COVER — black acrylic 6 mm",
          ["OD 260 / ID 120, ten countersunk M4",
           "65 × 15 magnet socket at 6 o'clock for the cloak mount"])

    sh.text(56, 1032, "docs/disc-build.md  ·  build-plans/render/disc_exploded.py", 10, "#8a9099", anchor="start")
    sh.text(56, 1050, "Geometry straight from disc-build.md. frame.md is a later divergence and should not be used.",
            10, "#8a9099", anchor="start")
    open("disc-exploded.svg", "w").write(sh.svg())
    print("wrote disc-exploded.svg")


main()

#!/usr/bin/env python3
"""Scale drawing of the Tron disc lower frame, generated from docs/frame.md.

Pure geometry, no image model: every arc and edge is the dimension in the spec.
Output: frame-plan.svg (mm units, 1:1). Rasterise with rsvg-convert.
"""
import math

# ---------------------------------------------------------------- spec (mm)
R_OUT, R_HOLE, R_RIM_IN = 130.0, 60.0, 114.0
R_INS_F, R_INS_B = 102.0, 80.0          # front / back M4 inserts
INSERT_OD = 8.0                          # nominal M4 wood-insert body
THICK = 24.0
WEDGES = (0.0, 120.0, 240.0)
BAY_COVERED = ((60.0, "BUTTONS"), (300.0, "ELECTRONICS"))
BAY_BATTERY = 180.0
COV_HALF, REAR_HALF, Y_STEP = 53.0, 39.0, 84.0
BLK_X0, BLK_X1, BLK_Y0, BLK_Y1 = 39.0, 53.0, 64.0, 84.0
COV_Y0, COV_Y1 = 61.0, 64.0
BAT_HALF, BAT_Y0, BAT_Y1 = 45.0, 66.0, 96.0
SLOT_R0, SLOT_R1 = 92.0, 100.0
TRIM_R = 66.0                            # see NOTES: relief at the 0 deg wedge tip
PROTO_Y = 70.5                           # protoboard face, 6x6x9.5 switches

Y_REAR = math.sqrt(R_RIM_IN**2 - REAR_HALF**2)      # 107.12
D_REAR = math.degrees(math.asin(REAR_HALF / R_RIM_IN))
D_TRIM = math.degrees(math.asin(COV_HALF / TRIM_R))  # 53.43 -> +/-6.58 off 0

INK, MAPLE, CUT = "#1b1b1b", "#e3cda0", "#ffffff"
BLUE, RED, GREEN, GREY = "#1f6fb4", "#c0392b", "#2e7d4f", "#8a8a8a"

# ------------------------------------------------------------- geometry help
def pol(cx, cy, r, phi):
    a = math.radians(phi)
    return (cx + r * math.sin(a), cy - r * math.cos(a))

def bay(cx, cy, A, x, y):
    a = math.radians(A)
    return (cx + y * math.sin(a) + x * math.cos(a),
            cy - y * math.cos(a) + x * math.sin(a))

def arc(cx, cy, r, a0, a1, step=0.4):
    n = max(2, int(abs(a1 - a0) / step) + 1)
    return [pol(cx, cy, r, a0 + (a1 - a0) * i / n) for i in range(n + 1)]

def path(pts, close=True):
    d = "M " + " L ".join(f"{x:.3f},{y:.3f}" for x, y in pts)
    return d + (" Z" if close else "")

def circle_path(cx, cy, r):
    return (f"M {cx-r:.3f},{cy:.3f} a {r},{r} 0 1,0 {2*r},0 "
            f"a {r},{r} 0 1,0 {-2*r},0 Z")

def covered_bay(cx, cy, A):
    p = [bay(cx, cy, A, -COV_HALF, 0.0), bay(cx, cy, A, -COV_HALF, Y_STEP),
         bay(cx, cy, A, -REAR_HALF, Y_STEP), bay(cx, cy, A, -REAR_HALF, Y_REAR)]
    p += arc(cx, cy, R_RIM_IN, A - D_REAR, A + D_REAR)
    p += [bay(cx, cy, A, REAR_HALF, Y_REAR), bay(cx, cy, A, REAR_HALF, Y_STEP),
          bay(cx, cy, A, COV_HALF, Y_STEP), bay(cx, cy, A, COV_HALF, 0.0)]
    return path(p)

def battery_bay(cx, cy):
    A = BAY_BATTERY
    return path([bay(cx, cy, A, -BAT_HALF, BAT_Y0), bay(cx, cy, A, -BAT_HALF, BAT_Y1),
                 bay(cx, cy, A,  BAT_HALF, BAT_Y1), bay(cx, cy, A,  BAT_HALF, BAT_Y0)])

def trim_sector(cx, cy):
    """Relief at the 0 deg wedge tip, where the two covered bays overrun."""
    p = arc(cx, cy, R_HOLE - 2, -D_TRIM - 1.5, D_TRIM + 1.5)
    p += list(reversed(arc(cx, cy, TRIM_R, -D_TRIM, D_TRIM)))
    return path(p)

def ring_sector(cx, cy, r0, r1, a0, a1):
    p = arc(cx, cy, r0, a0, a1) + list(reversed(arc(cx, cy, r1, a0, a1)))
    return path(p)

# ------------------------------------------------------------------- drawing
class Sheet:
    def __init__(self, w, h):
        self.w, self.h, self.o, self.defs = w, h, [], []
    def add(self, s): self.o.append(s)
    def define(self, s): self.defs.append(s)
    def text(self, x, y, s, size=4.2, fill=INK, anchor="middle", weight="400",
             style="", ls="0"):
        s = (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        self.add(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{fill}" '
                 f'text-anchor="{anchor}" font-weight="{weight}" letter-spacing="{ls}" '
                 f'font-family="Helvetica Neue,Helvetica,Arial,sans-serif" {style}>{s}</text>')
    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}mm" '
                f'height="{self.h}mm" viewBox="0 0 {self.w} {self.h}">\n'
                f'<rect width="{self.w}" height="{self.h}" fill="#ffffff"/>\n'
                f'<defs>\n' + "\n".join(self.defs) + '\n</defs>\n'
                + "\n".join(self.o) + "\n</svg>\n")


def frame_view(sh, cx, cy, back=False, tag="A"):
    """One plan view of the glued 4-layer frame."""
    uid = f"v{tag}"
    cuts = [circle_path(cx, cy, R_HOLE), trim_sector(cx, cy), battery_bay(cx, cy)]
    cuts += [covered_bay(cx, cy, A) for A, _ in BAY_COVERED]

    sh.define(f'<mask id="wood{uid}">'
              f'<path d="{circle_path(cx,cy,R_OUT)}" fill="#fff"/>'
              + "".join(f'<path d="{d}" fill="#000"/>' for d in cuts) + '</mask>')
    sh.define(f'<clipPath id="ann{uid}"><path d="{circle_path(cx,cy,R_OUT)} '
              f'{circle_path(cx,cy,R_HOLE)}" clip-rule="evenodd"/></clipPath>')

    g = f'<g transform="translate({2*cx:.3f},0) scale(-1,1)">' if back else '<g>'
    sh.add(g)
    # solid wood
    sh.add(f'<path d="{circle_path(cx,cy,R_OUT)}" fill="{MAPLE}" mask="url(#wood{uid})"/>')
    # cut edges: masked, so the stroke lands exactly on the boundary
    sh.add(f'<g mask="url(#wood{uid})" fill="none" stroke="{INK}" stroke-width="1.0">')
    for d in cuts + [circle_path(cx, cy, R_OUT)]:
        sh.add(f'<path d="{d}"/>')
    sh.add('</g>')
    # outer rim inner edge (reference only, no cut)
    sh.add(f'<path d="{circle_path(cx,cy,R_RIM_IN)}" fill="none" stroke="{GREY}" '
           f'stroke-width="0.35" stroke-dasharray="3,2" clip-path="url(#ann{uid})"/>')

    if not back:
        # blocks + covers, parts that get glued in
        for A, name in BAY_COVERED:
            for s in (-1, 1):
                sh.add(f'<path d="{path([bay(cx,cy,A,s*BLK_X0,BLK_Y0),bay(cx,cy,A,s*BLK_X1,BLK_Y0),bay(cx,cy,A,s*BLK_X1,BLK_Y1),bay(cx,cy,A,s*BLK_X0,BLK_Y1)])}" '
                       f'fill="#c9a86a" stroke="{INK}" stroke-width="0.5"/>')
            sh.add(f'<path d="{path([bay(cx,cy,A,-COV_HALF,COV_Y0),bay(cx,cy,A,COV_HALF,COV_Y0),bay(cx,cy,A,COV_HALF,COV_Y1),bay(cx,cy,A,-COV_HALF,COV_Y1)])}" '
                   f'fill="#2a2a2a" stroke="{INK}" stroke-width="0.4"/>')
    else:
        # wire slots: layer 4 only, 6 deep from the back
        for a0, a1 in ((-38, 38), (202, 278)):
            sh.add(f'<path d="{ring_sector(cx,cy,SLOT_R0,SLOT_R1,a0,a1)}" '
                   f'fill="{GREEN}" fill-opacity="0.22" stroke="{GREEN}" '
                   f'stroke-width="0.6" stroke-dasharray="4,2" mask="url(#wood{uid})"/>')

    # inserts
    live_r, live_c, dead_r, dead_c = ((R_INS_B, RED, R_INS_F, BLUE) if back
                                      else (R_INS_F, BLUE, R_INS_B, RED))
    for W in WEDGES:
        x, y = pol(cx, cy, dead_r, W)
        sh.add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{INSERT_OD/2}" fill="none" '
               f'stroke="{dead_c}" stroke-width="0.5" stroke-dasharray="2,1.6" opacity="0.65"/>')
        x, y = pol(cx, cy, live_r, W)
        sh.add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{INSERT_OD/2}" fill="{live_c}" '
               f'fill-opacity="0.18" stroke="{live_c}" stroke-width="1.0"/>')
        sh.add(f'<path d="M {x-5.5:.2f},{y:.2f} H {x+5.5:.2f} M {x:.2f},{y-5.5:.2f} '
               f'V {y+5.5:.2f}" stroke="{live_c}" stroke-width="0.45"/>')
    if not back:
        for A, _ in BAY_COVERED:          # 4 cover-block inserts, axis radial
            for s in (-1, 1):
                x, y = bay(cx, cy, A, s * 46.0, BLK_Y0)
                sh.add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.0" fill="none" '
                       f'stroke="{GREEN}" stroke-width="0.8"/>')
    sh.add('</g>')

    # ---- labels, drawn unmirrored on top
    def L(r, phi, s, size=4.0, fill=INK, w="400", dy=0.0):
        p = -phi if back else phi
        x, y = pol(cx, cy, r, p)
        sh.text(x, y + dy, s, size, fill, weight=w)

    for W in WEDGES:
        L(R_INS_F - 11 if not back else R_INS_B - 11, W,
          ("R102" if not back else "R80"), 4.0,
          BLUE if not back else RED, "700", dy=1.4)
    for A, name in BAY_COVERED:
        L(100, A, name, 4.0, "#6b5a36", "700")
        L(100, A, f"bay {A:.0f}°", 3.3, "#6b5a36", dy=5.0)
    L(112, BAY_BATTERY, "BATTERY", 4.0, "#6b5a36", "700")
    L(112, BAY_BATTERY, "bay 180°", 3.3, "#6b5a36", dy=5.0)
    for W, nm in zip(WEDGES, ("WEDGE 0°", "WEDGE 120°", "WEDGE 240°")):
        L(122, W, nm, 3.4, "#6b5a36", "700")

    # clock ticks
    for phi in range(0, 360, 30):
        p = -phi if back else phi
        x0, y0 = pol(cx, cy, R_OUT + 2.5, p)
        x1, y1 = pol(cx, cy, R_OUT + (7 if phi % 60 == 0 else 4.5), p)
        sh.add(f'<path d="M {x0:.2f},{y0:.2f} L {x1:.2f},{y1:.2f}" stroke="{GREY}" '
               f'stroke-width="{0.6 if phi%60==0 else 0.35}"/>')
        if phi % 60 == 0:
            x2, y2 = pol(cx, cy, R_OUT + 13, p)
            sh.text(x2, y2 + 1.4, f"{phi}°", 3.6, GREY)

    sh.text(cx, cy - 1, "HAND HOLE", 4.4, "#9a9a9a", weight="700", ls="1.2")
    sh.text(cx, cy + 5.5, "Ø120", 4.0, "#9a9a9a")
    sh.text(cx, cy + 12.5, "reach from the " + ("back" if back else "front"), 3.2, "#bbb")
    sh.text(cx, cy - 152, ("BACK VIEW" if back else "FRONT VIEW"), 7.0, INK,
            weight="700", ls="1.6")
    sh.text(cx, cy - 144.5,
            ("seen from the back — 3 back inserts R80, wire slots in layer 4"
             if back else
             "seen from the front — 3 front inserts R102, blocks and covers in place"),
            3.8, "#555")


def bay_detail(sh, DX, DY, s=1.9, yc=77.0):
    """One covered bay at larger scale, dimensioned in bay x / y."""
    def P(x, y):                       # bay coords -> sheet coords
        return (DX + s * x, DY - s * (y - yc))
    X0, X1, Y0, Y1 = -74.0, 74.0, 42.0, 112.0
    SLOT_W, SLOT_D = 1.8, 1.5          # protoboard slot in the block side face

    cut = [(-COV_HALF, Y0 - 6), (-COV_HALF, Y_STEP), (-REAR_HALF, Y_STEP),
           (-REAR_HALF, Y_REAR), (REAR_HALF, Y_REAR), (REAR_HALF, Y_STEP),
           (COV_HALF, Y_STEP), (COV_HALF, Y0 - 6)]
    hole = [(60 * math.sin(math.radians(t)), 60 * math.cos(math.radians(t)))
            for t in [i * 0.5 - 70 for i in range(281)]]

    sh.define(f'<mask id="dmask"><rect x="{P(X0,Y1)[0]:.2f}" y="{P(X0,Y1)[1]:.2f}" '
              f'width="{s*(X1-X0):.2f}" height="{s*(Y1-Y0):.2f}" fill="#fff"/>'
              f'<path d="{path([P(*q) for q in cut])}" fill="#000"/>'
              f'<path d="{path([P(*q) for q in hole]+[P(X1,Y0-10),P(X0,Y0-10)])}" fill="#000"/>'
              '</mask>')
    sh.add(f'<rect x="{P(X0,Y1)[0]:.2f}" y="{P(X0,Y1)[1]:.2f}" width="{s*(X1-X0):.2f}" '
           f'height="{s*(Y1-Y0):.2f}" fill="{MAPLE}" mask="url(#dmask)"/>')
    sh.add(f'<g mask="url(#dmask)" fill="none" stroke="{INK}" stroke-width="1.1">'
           f'<path d="{path([P(*q) for q in cut])}"/></g>')
    # R60 is only a reference here: the 106-wide opening swallows it, so a covered
    # bay has no hand-hole wall at all.
    sh.add(f'<path d="{path([P(*q) for q in hole if abs(q[0])<=70 and q[1]>=Y0], close=False)}" '
           f'fill="none" stroke="{GREY}" stroke-width="0.7" stroke-dasharray="4,2.5"/>')
    sh.add(f'<rect x="{P(X0,Y1)[0]:.2f}" y="{P(X0,Y1)[1]:.2f}" width="{s*(X1-X0):.2f}" '
           f'height="{s*(Y1-Y0):.2f}" fill="none" stroke="{GREY}" stroke-width="0.4"/>')

    for sg in (-1, 1):                 # blocks, their slots and their inserts
        a, b = P(sg * BLK_X0, BLK_Y1), P(sg * BLK_X1, BLK_Y0)
        sh.add(f'<rect x="{min(a[0],b[0]):.2f}" y="{min(a[1],b[1]):.2f}" '
               f'width="{abs(a[0]-b[0]):.2f}" height="{abs(a[1]-b[1]):.2f}" '
               f'fill="#c9a86a" stroke="{INK}" stroke-width="0.8"/>')
        c, d = P(sg * BLK_X0, PROTO_Y + SLOT_W / 2), P(sg * (BLK_X0 + SLOT_D), PROTO_Y - SLOT_W / 2)
        sh.add(f'<rect x="{min(c[0],d[0]):.2f}" y="{min(c[1],d[1]):.2f}" '
               f'width="{abs(c[0]-d[0]):.2f}" height="{abs(c[1]-d[1]):.2f}" '
               f'fill="{RED}" fill-opacity="0.45" stroke="{RED}" stroke-width="0.5"/>')
        # radial insert reads as a 10-long pocket in plan, not a circle
        e, f = P(sg * 46 - 4, BLK_Y0 + 10), P(sg * 46 + 4, BLK_Y0)
        sh.add(f'<rect x="{min(e[0],f[0]):.2f}" y="{min(e[1],f[1]):.2f}" '
               f'width="{abs(e[0]-f[0]):.2f}" height="{abs(e[1]-f[1]):.2f}" '
               f'fill="{GREEN}" fill-opacity="0.22" stroke="{GREEN}" stroke-width="1.0"/>')
        g0, g1 = P(sg * 46, BLK_Y0 + 10), P(sg * 60, 86.5)
        sh.add(f'<path d="M {g0[0]:.2f},{g0[1]:.2f} L {g1[0]:.2f},{g1[1]:.2f}" '
               f'stroke="{GREEN}" stroke-width="0.5" stroke-dasharray="2.5,1.5"/>')
        sh.text(*P(sg * 60.0, 88.5), f"M4 insert x = {sg*46:+.0f}", 3.3, GREEN, weight="700")
        sh.text(*P(sg * 46.0, BLK_Y0 - 4.5), "BLOCK 14×20×24", 2.9, "#6b5a36", weight="700")

    a, b = P(-COV_HALF, COV_Y1), P(COV_HALF, COV_Y0)
    sh.add(f'<rect x="{a[0]:.2f}" y="{a[1]:.2f}" width="{b[0]-a[0]:.2f}" '
           f'height="{b[1]-a[1]:.2f}" fill="#2a2a2a"/>')

    py = P(0, PROTO_Y)                 # protoboard, buttons bay only
    sh.add(f'<rect x="{P(-40,0)[0]:.2f}" y="{py[1]-s*0.9:.2f}" width="{s*80:.2f}" '
           f'height="{s*1.8:.2f}" fill="{RED}" fill-opacity="0.5" stroke="{RED}" stroke-width="0.7"/>')
    sh.text(*P(0, PROTO_Y + 3.6), "PROTOBOARD 80 × 20 on edge — buttons bay only, face at y = 70.5",
            3.0, RED, weight="700")
    sh.text(*P(0, 54.0), "R60 nominal hand hole — the 106-wide opening swallows it,", 3.0, "#777")
    sh.text(*P(0, 50.5), "so a covered bay has no hand-hole wall", 3.0, "#777")
    sh.text(*P(0, 46.0), "COVER 106 × 23.5 × 3 black acrylic, y = 61–64", 3.4, INK, weight="700")
    sh.text(*P(0, 42.8), "screws M4×12 countersunk at x = ±46", 3.0, "#555")

    def dim_h(y, x0, x1, label, off):
        p0, p1 = P(x0, y), P(x1, y)
        yy = p0[1] + off
        sh.add(f'<path d="M {p0[0]:.2f},{yy:.2f} H {p1[0]:.2f}" stroke="{INK}" '
               f'stroke-width="0.4" marker-start="url(#ar)" marker-end="url(#ar)"/>')
        sh.add(f'<path d="M {p0[0]:.2f},{p0[1]:.2f} V {yy:.2f} M {p1[0]:.2f},{p1[1]:.2f} V {yy:.2f}" '
               f'stroke="{GREY}" stroke-width="0.25"/>')
        sh.text((p0[0] + p1[0]) / 2, yy - 1.6, label, 3.2, INK, weight="700")
    dim_h(Y_REAR, -REAR_HALF, REAR_HALF, "78   rear part, |x| ≤ 39", 9)
    dim_h(Y_STEP, -COV_HALF, COV_HALF, "106   front part, |x| ≤ 53   (= cover length)", -7)

    def dim_v(x, y0, y1, label, off):
        p0, p1 = P(x, y0), P(x, y1)
        xx = p0[0] + off
        sh.add(f'<path d="M {xx:.2f},{p0[1]:.2f} V {p1[1]:.2f}" stroke="{INK}" '
               f'stroke-width="0.4" marker-start="url(#ar)" marker-end="url(#ar)"/>')
        sh.add(f'<path d="M {p0[0]:.2f},{p0[1]:.2f} H {xx:.2f} M {p1[0]:.2f},{p1[1]:.2f} H {xx:.2f}" '
               f'stroke="{GREY}" stroke-width="0.25"/>')
        sh.text(xx + 2.0, (p0[1] + p1[1]) / 2 + 1.1, label, 3.2, INK, weight="700", anchor="start")
    dim_v(COV_HALF, BLK_Y0, BLK_Y1, "y 64–84   block pocket", 11)
    dim_v(REAR_HALF, Y_STEP, Y_REAR, "y 84–107   out to R114", 44)

    sh.text(DX, DY - s * (Y1 - yc) - 8.0, "DETAIL — ONE COVERED BAY", 5.6, INK, weight="700", ls="1.2")
    sh.text(DX, DY - s * (Y1 - yc) - 3.0,
            "identical at 60° (buttons) and 300° (electronics) · bay x / y · hand hole at the bottom",
            3.4, "#555")


def leader(sh, cx, cy, back, r0, phi, r1, lines, col=INK, size=3.5):
    """Arrow on the feature, elbow outside the disc, text clear of the drawing."""
    p = -phi if back else phi
    x0, y0 = pol(cx, cy, r0, p)
    x1, y1 = pol(cx, cy, r1, p)
    tail = 7.0 if x1 >= cx else -7.0
    x2 = x1 + tail
    sh.add(f'<path d="M {x0:.2f},{y0:.2f} L {x1:.2f},{y1:.2f} L {x2:.2f},{y1:.2f}" '
           f'fill="none" stroke="{col}" stroke-width="0.4" marker-start="url(#ar)"/>')
    anchor = "start" if tail > 0 else "end"
    tx = x2 + (1.8 if tail > 0 else -1.8)
    for i, ln in enumerate(lines):
        sh.text(tx, y1 + 1.2 + i * 4.3, ln, size if i == 0 else size - 0.5, col,
                anchor=anchor, weight=("700" if i == 0 else "400"))


def main():
    sh = Sheet(800, 622)
    sh.define(f'<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" '
              f'markerHeight="5" orient="auto-start-reverse">'
              f'<path d="M 0,1 L 10,5 L 0,9 z" fill="{INK}"/></marker>')

    # header
    sh.add('<rect x="0" y="0" width="800" height="40" fill="#15202b"/>')
    sh.text(26, 21, "TRON IDENTITY DISC — LOWER FRAME", 11.5, "#ffffff", anchor="start",
            weight="700", ls="2.2")
    sh.text(26, 31.5, "4 × 6 mm maple plywood, glued to 24 thick · Ø260 / Ø120 · "
            "generated 1:1 from docs/frame.md", 4.4, "#8fb6d6", anchor="start")
    sh.text(774, 20, "SHEET 1 — FRAME", 6.4, "#ffffff", anchor="end", weight="700", ls="1.2")
    sh.text(774, 30.5, "all dimensions mm · angles clockwise from 12 o'clock, seen from the front",
            3.6, "#8fb6d6", anchor="end")

    frame_view(sh, 215, 238, back=False, tag="F")
    frame_view(sh, 585, 238, back=True, tag="B")
    leader(sh, 215, 238, False, R_OUT, 203, 150,
           ["Ø260 OUTER EDGE", "outer rim R114–R130, no openings"], INK)
    leader(sh, 215, 238, False, R_RIM_IN, 223, 150,
           ["R114 RIM INNER EDGE", "reference only — not a cut"], GREY)
    for a in (34.0, 252.0):
        leader(sh, 585, 238, True, 96, a, 150,
               ["WIRE SLOT R92–R100", "layer 4 only, 6 deep from the back"], GREEN)
    bay_detail(sh, 232, 478)

    # legend
    lx, ly = 452, 404
    sh.text(lx, ly, "KEY", 5.0, INK, anchor="start", weight="700", ls="1.4")
    items = ((MAPLE, INK, "Solid plywood (all 4 layers)"),
             ("#ffffff", INK, "Cut through all 4 layers"),
             ("#c9a86a", INK, "Glued-in block, 14 × 20 × 24"),
             ("#2a2a2a", INK, "3 mm black acrylic cover"),
             (BLUE, BLUE, "M4 insert, FRONT face  (R102 @ 0/120/240)"),
             (RED, RED, "M4 insert, BACK face  (R80 @ 0/120/240)"),
             (GREEN, GREEN, "M4 insert in block, radial  (x = ±46, 4 off)"),
             ("#9fd3b4", GREEN, "Wire slot R92–R100, layer 4 only, 6 deep"))
    for i, (f, s, t) in enumerate(items):
        y = ly + 9 + i * 8.2
        sh.add(f'<rect x="{lx}" y="{y-4.4}" width="7" height="6" fill="{f}" '
               f'stroke="{s}" stroke-width="0.6"/>')
        sh.text(lx + 11, y, t, 3.7, "#333", anchor="start")

    # notes
    nx, ny = 452, 492
    sh.text(nx, ny, "NOTES — CHECKED AGAINST docs/frame.md", 5.0, INK, anchor="start",
            weight="700", ls="1.2")
    notes = [
        ("1", "0° WEDGE TIP IS RELIEVED TO R66.", RED,
         "Both covered bays run 106 wide to the hand hole, so their walls cross on the 0° axis at",
         "R61.20 — the bays merge and the wedge ends in a knife point. frame.md calls this a “sliver",
         "R60 to about R65”; it is not a sliver. Cut the relief arc at R66, ±6.58° (15.2 mm).",
         "R66 is a choice: R62 removes the cusp but still leaves a 2.7 mm tip; R66 gives a 15.2 mm blunt end."),
        ("2", "BATTERY BAY HAND-HOLE WALL IS 6.0 mm AT 180°.", RED,
         "Thinnest point in the frame, 24 tall, cross-grain in two of the four layers. Moving the bay",
         "to y = 70 gives a 10 mm wall and still clears an 80 × 22 holder. Decision needed.", ""),
        ("3", "INSERT CLEARANCE HOLDS, BUT ONLY JUST AT R80.", GREEN,
         "Measured perpendicular to the bay wall, not along the arc (Codex’s correction): a back insert",
         "at R80 is 80·sin60° − 53 = 16.28 mm from the covered-bay front wall — 12.3 mm of wood from an",
         "8 mm-OD bore. A front insert at R102 has 35.33 mm to the bay and 28.00 mm to the outer edge.",
         "Front and back never meet: 22 mm apart radially, and z 0–10 against z 14–24."),
        ("4", "WIRE SLOTS OVERLAP THE R102 INSERTS IN PLAN ONLY.", GREY,
         "Slot R92–R100 vs an 8 mm insert body at R98–R106. No conflict in z: the front insert ends",
         "at z = 10, layer 4 starts at z = 18. 8 mm of solid wood between them.", ""),
        ("5", "BLOCK INSERTS ARE THE TIGHTEST FIT ON THE SHEET.", RED,
         "The block is 14 wide and the protoboard slot takes 1.5 off its inner face, leaving 12.5 mm of",
         "wood at x = 40.5–53. An 8 mm-OD insert at x = ±46 leaves only 1.5 mm to the slot. Use a 6 mm-OD",
         "hex-drive M4 insert (2.5 mm to the slot, 4 mm outboard) in solid hardwood, not laminated ply."),
        ("6", "CONFIRMED FROM THE SPEC.", GREY,
         "Rear corner |x| = 39 meets R114 at y = 107.12. Battery corner R106.02. Cover end sits 32.9 mm",
         "behind the hand-hole edge. Wedge is 51.7 mm wide at R80. Outer rim R114–R130 unbroken.", ""),
    ]
    y = ny + 9
    for num, head, col, *body in notes:
        sh.text(nx, y, num, 3.9, col, anchor="start", weight="700")
        sh.text(nx + 6, y, head, 3.9, col, anchor="start", weight="700")
        y += 4.6
        for line in body:
            if line:
                sh.text(nx + 6, y, line, 3.5, "#444", anchor="start")
                y += 4.3
        y += 2.6

    sh.add('<rect x="0" y="612" width="800" height="10" fill="#15202b"/>')
    sh.text(26, 618.6, "build-plans/render/frame_render.py  ·  regenerate with:  "
            "python3 frame_render.py && rsvg-convert -z 4 frame-plan.svg -o frame-plan.png",
            3.5, "#8fb6d6", anchor="start")

    open("frame-plan.svg", "w").write(sh.svg())
    print("wrote frame-plan.svg")


if __name__ == "__main__":
    main()

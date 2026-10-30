#!/usr/bin/env python3
"""Lower frame, rev 2 — arc-hugging pockets sized to the components.

Replaces the chord-based bays of rev 1. Everything the user touches sits on the
hand-hole arc; pockets are component-sized; geometry is router-ready for a
5/16" guide bushing + 1/8" bit working to a laser-cut acrylic template.
"""
import math

# ------------------------------------------------------------------ geometry
R_OUT, R_HOLE, R_RIM_IN = 130.0, 60.0, 114.0
R_COVER = 63.0                      # back face of the 3 mm cover
R_INS_F, R_INS_B, INSERT_OD = 102.0, 80.0, 8.0
WEDGES = (0.0, 120.0, 240.0)
THICK = 24.0

# router: 5/16" OD bushing, 1/8" bit
BUSH, BIT = 5 / 16 * 25.4, 1 / 8 * 25.4
TOFF = (BUSH - BIT) / 2             # 2.38125 template offset
RCORNER = BIT / 2                   # 1.5875 finished inside corner

# bays: (name, component span, cover span, pocket outer R, colour key)
BAY_BTN = dict(name="BUTTONS", a0=30.0, a1=90.0, c0=24.0, c1=96.0, rout=80.0,
               facets=[(30, 50), (50, 70), (70, 90)])
BAY_ELE = dict(name="ELECTRONICS", a0=265.0, a1=335.0, c0=259.0, c1=341.0, rout=93.0,
               facets=[(265, 282.5), (282.5, 300), (300, 317.5), (317.5, 335)])
BAYS = [BAY_BTN, BAY_ELE]

BAT_A = 180.0                        # battery: a rigid cell must stay a chord
BAT_HALF, BAT_Y0, BAT_Y1 = 41.0, 69.0, 92.0

BUTTONS = [36.0, 44.0, 56.0, 64.0]   # Codex packing
SWITCH_A, SWITCH_W = 80.0, 10.0
BOARDS = [  # (label, centre angle, tangential width, r_in, r_out, radial?, port?)
    ("ESP32-C3", 275.0, 18.0, 63.0, 85.5, True, True),
    ("TP4056", 292.0, 17.0, 63.0, 91.0, True, True),
    ("HALL", 302.75, 5.0, 63.0, 72.0, True, False),
    ("MT3608", 320.0, 36.0, 70.0, 87.0, False, False),
]

INK, MAPLE, CUT = "#1b1b1b", "#e3cda0", "#ffffff"
BLUE, RED, GREEN, GREY, MAG = "#1f6fb4", "#c0392b", "#2e7d4f", "#8a8a8a", "#b5179e"

def pol(cx, cy, r, phi):
    a = math.radians(phi)
    return (cx + r * math.sin(a), cy - r * math.cos(a))

def bay(cx, cy, A, x, y):
    a = math.radians(A)
    return (cx + y * math.sin(a) + x * math.cos(a),
            cy - y * math.cos(a) + x * math.sin(a))

def arc(cx, cy, r, a0, a1, step=0.35):
    n = max(2, int(abs(a1 - a0) / step) + 1)
    return [pol(cx, cy, r, a0 + (a1 - a0) * i / n) for i in range(n + 1)]

def path(pts, close=True):
    return "M " + " L ".join(f"{x:.3f},{y:.3f}" for x, y in pts) + (" Z" if close else "")

def circle_path(cx, cy, r):
    return f"M {cx-r:.3f},{cy:.3f} a {r},{r} 0 1,0 {2*r},0 a {r},{r} 0 1,0 {-2*r},0 Z"

def facet_pts(cx, cy, r, a0, a1, facets):
    """Inner boundary as flat chords, each tangent to radius r at its midpoint."""
    pts = []
    for f0, f1 in facets:
        half = math.radians((f1 - f0) / 2)
        rr = r / math.cos(half)                 # chord ends sit this far out
        pts += [pol(cx, cy, rr, f0), pol(cx, cy, rr, f1)]
    return pts

def pocket(cx, cy, b):
    """Stepped opening: cover rebate R60-R63 over the cover span, component
    pocket R63-rout over the component span."""
    p = [pol(cx, cy, R_HOLE - 4, b["c0"])]
    p += arc(cx, cy, R_HOLE - 4, b["c0"], b["c1"])
    p += [pol(cx, cy, R_COVER, b["c1"]), pol(cx, cy, R_COVER, b["a1"])]
    p += arc(cx, cy, b["rout"], b["a1"], b["a0"])
    p += [pol(cx, cy, R_COVER, b["a0"]), pol(cx, cy, R_COVER, b["c0"])]
    return path(p)

def battery_pocket(cx, cy):
    return path([bay(cx, cy, BAT_A, -BAT_HALF, BAT_Y0), bay(cx, cy, BAT_A, -BAT_HALF, BAT_Y1),
                 bay(cx, cy, BAT_A,  BAT_HALF, BAT_Y1), bay(cx, cy, BAT_A,  BAT_HALF, BAT_Y0)])

def offset_sector(cx, cy, r0, r1, a0, a1, d, n=26):
    """Exact outward offset of an annular sector by d — the template aperture."""
    def dphi(r): return math.degrees(math.asin(min(1.0, d / r)))
    ri, ro = r0 - d, r1 + d
    p = arc(cx, cy, ri, a0 - dphi(ri), a1 + dphi(ri))
    p += [pol(cx, cy, ri + (ro - ri) * i / n, a1 + dphi(ri + (ro - ri) * i / n))
          for i in range(n + 1)]
    p += arc(cx, cy, ro, a1 + dphi(ro), a0 - dphi(ro))
    p += [pol(cx, cy, ro - (ro - ri) * i / n, a0 - dphi(ro - (ro - ri) * i / n))
          for i in range(n + 1)]
    return path(p)

def board_poly(cx, cy, A, w, r0, r1, radial):
    if radial:
        h = math.degrees(math.asin(w / 2 / ((r0 + r1) / 2)))
        return path([pol(cx, cy, r0, A - h), pol(cx, cy, r1, A - h),
                     pol(cx, cy, r1, A + h), pol(cx, cy, r0, A + h)])
    return path([bay(cx, cy, A, -w / 2, r0), bay(cx, cy, A, -w / 2, r1),
                 bay(cx, cy, A,  w / 2, r1), bay(cx, cy, A,  w / 2, r0)])


class Sheet:
    def __init__(self, w, h):
        self.w, self.h, self.o, self.defs = w, h, [], []
    def add(self, s): self.o.append(s)
    def define(self, s): self.defs.append(s)
    def text(self, x, y, s, size=4.2, fill=INK, anchor="middle", weight="400", ls="0"):
        s = str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.add(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{fill}" '
                 f'text-anchor="{anchor}" font-weight="{weight}" letter-spacing="{ls}" '
                 f'font-family="Helvetica Neue,Helvetica,Arial,sans-serif">{s}</text>')
    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}mm" height="{self.h}mm" '
                f'viewBox="0 0 {self.w} {self.h}">\n<rect width="{self.w}" height="{self.h}" '
                f'fill="#ffffff"/>\n<defs>\n' + "\n".join(self.defs) + '\n</defs>\n'
                + "\n".join(self.o) + "\n</svg>\n")


def draw_frame(sh, cx, cy, uid, components=True, template=True):
    cuts = [circle_path(cx, cy, R_HOLE), battery_pocket(cx, cy)] + \
           [pocket(cx, cy, b) for b in BAYS]
    sh.define(f'<mask id="w{uid}"><path d="{circle_path(cx,cy,R_OUT)}" fill="#fff"/>'
              + "".join(f'<path d="{d}" fill="#000"/>' for d in cuts) + '</mask>')

    sh.add(f'<path d="{circle_path(cx,cy,R_OUT)}" fill="{MAPLE}" mask="url(#w{uid})"/>')
    sh.add(f'<g mask="url(#w{uid})" fill="none" stroke="{INK}" stroke-width="1.0">')
    for d in cuts + [circle_path(cx, cy, R_OUT)]:
        sh.add(f'<path d="{d}"/>')
    sh.add('</g>')
    sh.add(f'<path d="{circle_path(cx,cy,R_RIM_IN)}" fill="none" stroke="{GREY}" '
           f'stroke-width="0.3" stroke-dasharray="3,2"/>')

    if template:   # acrylic template aperture = finished pocket grown by 2.38125
        for b in BAYS:
            sh.add(f'<path d="{offset_sector(cx,cy,R_COVER,b["rout"],b["a0"],b["a1"],TOFF)}" '
                   f'fill="none" stroke="{MAG}" stroke-width="0.6" stroke-dasharray="3.5,2"/>')
            sh.add(f'<path d="{offset_sector(cx,cy,R_HOLE,R_COVER,b["c0"],b["c1"],TOFF)}" '
                   f'fill="none" stroke="{MAG}" stroke-width="0.45" stroke-dasharray="2.5,1.8"/>')
        sh.add(f'<path d="{path([bay(cx,cy,BAT_A,-BAT_HALF-TOFF,BAT_Y0-TOFF),bay(cx,cy,BAT_A,-BAT_HALF-TOFF,BAT_Y1+TOFF),bay(cx,cy,BAT_A,BAT_HALF+TOFF,BAT_Y1+TOFF),bay(cx,cy,BAT_A,BAT_HALF+TOFF,BAT_Y0-TOFF)])}" '
               f'fill="none" stroke="{MAG}" stroke-width="0.6" stroke-dasharray="3.5,2"/>')

    # covers: faceted 3 mm black acrylic, inner face on the hand-hole arc
    for b in BAYS:
        inner = facet_pts(cx, cy, R_HOLE, b["c0"], b["c1"],
                          [(b["c0"], b["facets"][0][0])] + b["facets"] + [(b["facets"][-1][1], b["c1"])])
        outer = facet_pts(cx, cy, R_COVER, b["c0"], b["c1"],
                          [(b["c0"], b["facets"][0][0])] + b["facets"] + [(b["facets"][-1][1], b["c1"])])
        sh.add(f'<path d="{path(inner + list(reversed(outer)))}" fill="#2a2a2a" '
               f'stroke="{INK}" stroke-width="0.4"/>')
        for f0, f1 in b["facets"][1:]:        # facet joints
            x0, y0 = pol(cx, cy, R_HOLE - 1, f0); x1, y1 = pol(cx, cy, R_COVER + 1, f0)
            sh.add(f'<path d="M {x0:.2f},{y0:.2f} L {x1:.2f},{y1:.2f}" stroke="#777" stroke-width="0.35"/>')

    if components:
        for lbl, A, w, r0, r1, radial, port in BOARDS:
            col = RED if port else "#7a5c2e"
            sh.add(f'<path d="{board_poly(cx,cy,A,w,r0,r1,radial)}" fill="{col}" '
                   f'fill-opacity="0.26" stroke="{col}" stroke-width="0.7"/>')
            if port:                            # USB-C mouth, on the arc
                h = math.degrees(math.asin(4.5 / r0))
                sh.add(f'<path d="{path(arc(cx,cy,R_HOLE+1.2,A-h,A+h), close=False)}" '
                       f'fill="none" stroke="{RED}" stroke-width="2.2"/>')
        for a in BUTTONS:                       # button tips land on R60
            x, y = pol(cx, cy, R_HOLE + 1.5, a)
            sh.add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.0" fill="{BLUE}" '
                   f'fill-opacity="0.35" stroke="{BLUE}" stroke-width="0.7"/>')
        h = math.degrees(math.asin(SWITCH_W / 2 / R_HOLE))
        sh.add(f'<path d="{path(arc(cx,cy,R_HOLE+1.5,SWITCH_A-h,SWITCH_A+h), close=False)}" '
               f'fill="none" stroke="{BLUE}" stroke-width="2.6"/>')
        # battery holder
        sh.add(f'<path d="{path([bay(cx,cy,BAT_A,-40,70),bay(cx,cy,BAT_A,-40,91),bay(cx,cy,BAT_A,40,91),bay(cx,cy,BAT_A,40,70)])}" '
               f'fill="{GREEN}" fill-opacity="0.20" stroke="{GREEN}" stroke-width="0.7"/>')

    # inserts
    for W in WEDGES:
        for r, c, dash in ((R_INS_F, BLUE, None), (R_INS_B, RED, "2,1.6")):
            x, y = pol(cx, cy, r, W)
            extra = f' stroke-dasharray="{dash}"' if dash else ''
            sh.add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{INSERT_OD/2}" fill="{c}" '
                   f'fill-opacity="0.15" stroke="{c}" stroke-width="0.9"{extra}/>')
            sh.add(f'<path d="M {x-5:.2f},{y:.2f} H {x+5:.2f} M {x:.2f},{y-5:.2f} V {y+5:.2f}" '
                   f'stroke="{c}" stroke-width="0.4"/>')
    for b in BAYS:                              # cover screw inserts, into solid frame
        for a in ((b["c0"] + b["a0"]) / 2, (b["c1"] + b["a1"]) / 2):
            x, y = pol(cx, cy, R_COVER + 5, a)
            sh.add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.0" fill="none" '
                   f'stroke="{GREEN}" stroke-width="1.0"/>')
            x0, y0 = pol(cx, cy, R_HOLE, a)
            sh.add(f'<path d="M {x0:.2f},{y0:.2f} L {x:.2f},{y:.2f}" stroke="{GREEN}" '
                   f'stroke-width="0.5" stroke-dasharray="2,1.4"/>')


FCX, FCY = 215.0, 310.0


def zoom(sh, uid, bx0, by0, bx1, by1, a0, a1, r0, r1, title, sub, pad=12.0):
    """Detail view auto-fitted to a polar region of the front view."""
    pts = [pol(FCX, FCY, r, a0 + (a1 - a0) * i / 40) for i in range(41) for r in (r0, r1)]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    cxr, cyr = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    k = min((bx1 - bx0 - pad) / (max(xs) - min(xs)), (by1 - by0 - pad) / (max(ys) - min(ys)))
    DX, DY = (bx0 + bx1) / 2, (by0 + by1) / 2
    sh.define(f'<clipPath id="c{uid}"><rect x="{bx0}" y="{by0}" width="{bx1-bx0}" '
              f'height="{by1-by0}" rx="2"/></clipPath>')
    sh.add(f'<g clip-path="url(#c{uid})"><rect x="{bx0}" y="{by0}" width="{bx1-bx0}" '
           f'height="{by1-by0}" fill="#fcfcfc"/><g transform="translate({DX:.3f},{DY:.3f}) '
           f'scale({k:.4f}) translate({-cxr:.3f},{-cyr:.3f})">')
    draw_frame(sh, FCX, FCY, uid)
    sh.add('</g></g>')
    sh.add(f'<rect x="{bx0}" y="{by0}" width="{bx1-bx0}" height="{by1-by0}" rx="2" '
           f'fill="none" stroke="{GREY}" stroke-width="0.5"/>')
    sh.text((bx0 + bx1) / 2, by0 - 7.5, title, 5.6, INK, weight="700", ls="1.2")
    sh.text((bx0 + bx1) / 2, by0 - 2.6, sub, 3.4, "#555")

    def at(r, phi):
        x, y = pol(FCX, FCY, r, phi)
        return (DX + k * (x - cxr), DY + k * (y - cyr))
    return at


def main():
    sh = Sheet(880, 706)
    sh.define(f'<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" '
              f'markerHeight="5" orient="auto-start-reverse"><path d="M 0,1 L 10,5 L 0,9 z" fill="{INK}"/></marker>')
    sh.add('<rect x="0" y="0" width="880" height="44" fill="#15202b"/>')
    sh.text(26, 21, "TRON IDENTITY DISC — LOWER FRAME, REV 2", 11.0, "#fff", anchor="start", weight="700", ls="2.0")
    sh.text(26, 32, "component-sized pockets on the hand-hole arc · routed from a laser-cut acrylic "
            "template · 5/16\" bushing + 1/8\" bit · 1:1", 4.3, "#8fb6d6", anchor="start")
    sh.add('<rect x="700" y="9" width="156" height="26" rx="3" fill="#b5179e"/>')
    sh.text(778, 20, "DRAFT", 11.0, "#fff", weight="700", ls="3")
    sh.text(778, 30, "not for cutting — joint review", 3.4, "#ffd9f3")

    draw_frame(sh, FCX, FCY, "F")
    sh.text(FCX, FCY, "HAND HOLE", 4.4, "#9a9a9a", weight="700", ls="1.2")
    sh.text(FCX, FCY + 6, "Ø120", 4.0, "#9a9a9a")
    sh.text(FCX, FCY - 158, "FRONT VIEW", 7.0, INK, weight="700", ls="1.6")
    sh.text(FCX, FCY - 150.5, "seen from the front · angles clockwise from 12 o'clock", 3.7, "#555")
    for phi in range(0, 360, 30):
        x0, y0 = pol(FCX, FCY, R_OUT + 2.5, phi)
        x1, y1 = pol(FCX, FCY, R_OUT + (7 if phi % 60 == 0 else 4.5), phi)
        sh.add(f'<path d="M {x0:.2f},{y0:.2f} L {x1:.2f},{y1:.2f}" stroke="{GREY}" '
               f'stroke-width="{0.6 if phi%60==0 else 0.3}"/>')
        if phi % 60 == 0:
            x2, y2 = pol(FCX, FCY, R_OUT + 13, phi)
            sh.text(x2, y2 + 1.4, f"{phi}°", 3.6, GREY)
    for b in BAYS:                      # mark the pocket's angular limits
        for a in (b["a0"], b["a1"]):
            x0, y0 = pol(FCX, FCY, b["rout"], a); x1, y1 = pol(FCX, FCY, R_OUT + 1, a)
            sh.add(f'<path d="M {x0:.2f},{y0:.2f} L {x1:.2f},{y1:.2f}" stroke="{GREY}" '
                   f'stroke-width="0.3" stroke-dasharray="2,2"/>')
            x2, y2 = pol(FCX, FCY, 120, a)
            sh.text(x2, y2 + 1.2, f"{a:.0f}°", 3.3, "#6b5a36", weight="700")
    for A, nm in ((60, "BUTTONS"), (300, "ELECTRONICS"), (180, "BATTERY")):
        x, y = pol(FCX, FCY, 107, A); sh.text(x, y, nm, 3.9, "#6b5a36", weight="700")
    for W, nm in zip(WEDGES, ("WEDGE 0°", "WEDGE 120°", "WEDGE 240°")):
        x, y = pol(FCX, FCY, R_INS_F - 11, W); sh.text(x, y + 1.3, "R102", 3.6, BLUE, weight="700")
        x, y = pol(FCX, FCY, R_INS_B - 10, W); sh.text(x, y + 1.3, "R80", 3.4, RED, weight="700")

    # ---- buttons detail
    at = zoom(sh, "B", 430, 92, 858, 300, 22, 98, 56, 86,
              "DETAIL — BUTTONS BAY",
              "pocket 30°–90°, R63–R80 · cover 24°–96° · every tip and the switch land on R60")
    for a in BUTTONS:
        x, y = at(55, a); sh.text(x, y, f"{a:.0f}°", 3.6, BLUE, weight="700")
    x, y = at(55, SWITCH_A); sh.text(x, y, "80° switch", 3.6, BLUE, weight="700")
    x, y = at(74, 55); sh.text(x, y, "boards R63–R75", 3.6, "#444", weight="700")
    x, y = at(74, 55); sh.text(x, y + 4.2, "2 short boards", 3.1, "#666")
    for a in (26.0, 94.0):
        x, y = at(86, a); sh.text(x, y, "M4 insert", 3.3, GREEN, weight="700")
        x, y = at(86, a); sh.text(x, y + 3.9, "into solid frame", 2.9, GREEN)

    # ---- electronics detail
    at = zoom(sh, "E", 430, 350, 858, 572, 255, 345, 56, 99,
              "DETAIL — ELECTRONICS BAY",
              "pocket 265°–335°, R63–R93 · each board aimed down its own radius · both USB-C mouths on R60")
    for lbl, A, w, r0, r1, radial, port in BOARDS:
        rr = 101 if lbl == "HALL" else (r0 + r1) / 2
        x, y = at(rr, A)
        sh.text(x, y, lbl, 3.6, RED if port else "#7a5c2e", weight="700")
        sh.text(x, y + 4.2, f"{A:.1f}°  R{r0:.0f}–R{r1:.0f}", 3.0, "#555")
        if lbl == "HALL":
            a0, b0 = at(72, A); sh.text(x, y - 3.8, "↓ 5×10 reservation", 2.8, "#7a5c2e")
        if port:
            px, py = at(52, A); sh.text(px, py, "USB-C", 3.3, RED, weight="700")
    for a in (261.0, 339.0):
        x, y = at(101, a); sh.text(x, y, "M4 insert", 3.3, GREEN, weight="700")

    # ---- key + notes
    ly = 592
    sh.text(26, ly, "KEY", 4.8, INK, anchor="start", weight="700", ls="1.4")
    for i, (f, s, t) in enumerate((
            (MAPLE, INK, "Solid plywood"), (CUT, INK, "Routed away"),
            ("#2a2a2a", INK, "3 mm faceted acrylic cover, inner face on R60"),
            ("#ffffff", MAG, "TEMPLATE aperture = finished pocket + 2.3813"),
            (RED, RED, "Board with USB-C; bar on R60 is the port mouth"),
            ("#7a5c2e", "#7a5c2e", "Board, no port"),
            (BLUE, BLUE, "Button tip / slide switch, on R60"),
            (GREEN, GREEN, "18650 holder · M4 cover-screw insert in solid frame"))):
        y = ly + 8 + i * 7.2
        sh.add(f'<rect x="26" y="{y-4.0}" width="6.5" height="5.4" fill="{f}" stroke="{s}" stroke-width="0.6"/>')
        sh.text(36, y, t, 3.5, "#333", anchor="start")

    nx = 320
    sh.text(nx, ly, "WHAT CHANGED, AND WHY", 4.8, INK, anchor="start", weight="700", ls="1.2")
    notes = [
        ("Chords are gone.", RED,
         "Rev 1 put the cover and the 80 mm board on straight lines tangent to a round hole. The cover ends finished",
         "32.9 mm behind the hand-hole edge, the board ends 25.8 mm, and the opening ate 124° of the hole per bay."),
        ("No blocks, no chisel.", GREEN,
         "The four glued 14×20×24 blocks are deleted. The cover is longer than its pocket and overlaps solid frame at",
         "both ends; the M4 insert is drilled radially into that frame at R63. That removes 4 blocks, 8 square corners,",
         "the glue-up, and the 1.8 mm protoboard slot that was too narrow to route."),
        ("Router-ready.", MAG,
         "Magenta is the acrylic template aperture — the finished pocket grown by 2.3813 all round. Every inside corner",
         "finishes at R1.5875 by design, not by chisel. No aperture under 7.938 wide, no finished pocket under 3.175."),
        ("The battery is the exception.", GREY,
         "A cell is rigid so it stays a chord, and it needs no hand-hole opening — it is reached from the back. Moved out",
         "to y = 69, so the hand-hole wall goes 6.0 → 9.0 mm. Its corners reach R100.7, the only thing outside R93."),
        ("Not validated — do not assume.", RED,
         "MOSFET board has no reserved space (dimensions unknown). One routed sheet or four glued layers? Through-cuts",
         "or blind pockets? C-channel radii still differ by 1 mm between front-face.md and disc-build.md. The cover",
         "spans ~75 mm between its two screws — check 3 mm acrylic does not bow when a button is pressed. And the",
         "Hall reservation clears the MT3608 by only 0.71° — about 0.9 mm at R72."),
    ]
    y = ly + 8
    for head, col, *body in notes:
        sh.text(nx, y, head, 3.8, col, anchor="start", weight="700"); y += 4.3
        for ln in body:
            sh.text(nx, y, ln, 3.3, "#444", anchor="start"); y += 3.9
        y += 2.0

    sh.add('<rect x="0" y="696" width="880" height="10" fill="#15202b"/>')
    sh.text(26, 702.6, "build-plans/render/frame_render_v2.py  ·  python3 frame_render_v2.py && "
            "rsvg-convert -w 2600 frame-plan-v2.svg -o frame-plan-v2.png", 3.3, "#8fb6d6", anchor="start")
    open("frame-plan-v2.svg", "w").write(sh.svg())
    print("wrote frame-plan-v2.svg")


main()

#!/usr/bin/env python3
"""Lower frame, rev 3 — FLAT covers (Brennan, 2026-10-29).

Rev 2's faceted covers are replaced by one flat plate per bay. Flat works here
because each cover is short: the notch is sized to its features, and the cover
overruns it by 8 mm each side onto solid frame for the screws. Everything a
finger or a cable reaches is within 6 mm of the hand-hole edge.
"""
import math

R_OUT, R_HOLE, R_RIM_IN = 130.0, 60.0, 114.0
R_INS_F, R_INS_B, INSERT_OD = 102.0, 80.0, 8.0
WEDGES = (0.0, 120.0, 240.0)
COV_Y0, COV_Y1 = 61.0, 64.0
BUSH, BIT = 5 / 16 * 25.4, 1 / 8 * 25.4
TOFF, RCORNER = (BUSH - BIT) / 2, BIT / 2

BAYS = [
    dict(name="BUTTONS", A=60.0, notch=35.0, cover=35.0, ear=28.0,
         pocket=[(21.0, 64.0, 84.0)],
         buttons=[-16.5, -5.5, 5.5, 16.5], switch=None),
    dict(name="ELECTRONICS", A=300.0, notch=38.0, cover=38.0, ear=31.0,
         pocket=[(24.0, 64.0, 87.0), (20.0, 87.0, 92.0)],
         buttons=[], switch=None),
]
BOARDS = [  # bay index, label, x0, x1, y0, y1, has USB-C at y0
    (0, "BUTTON BOARD 38×20 on edge", -19.0, 19.0, 68.5, 70.3, False),
    (1, "ESP32-C3", -21.0, -3.0, 64.0, 86.5, True),
    (1, "TP4056", 1.0, 18.0, 64.0, 92.0, True),
]
BAT_A, BAT_HALF, BAT_Y0, BAT_Y1 = 180.0, 41.0, 69.0, 92.0

INK, MAPLE, CUT = "#1b1b1b", "#e3cda0", "#ffffff"
BLUE, RED, GREEN, GREY, MAG = "#1f6fb4", "#c0392b", "#2e7d4f", "#8a8a8a", "#b5179e"

def pol(cx, cy, r, phi):
    a = math.radians(phi); return (cx + r * math.sin(a), cy - r * math.cos(a))
def bay(cx, cy, A, x, y):
    a = math.radians(A)
    return (cx + y * math.sin(a) + x * math.cos(a), cy - y * math.cos(a) + x * math.sin(a))
def arc(cx, cy, r, a0, a1, step=0.35):
    n = max(2, int(abs(a1 - a0) / step) + 1)
    return [pol(cx, cy, r, a0 + (a1 - a0) * i / n) for i in range(n + 1)]
def path(pts, close=True):
    return "M " + " L ".join(f"{x:.3f},{y:.3f}" for x, y in pts) + (" Z" if close else "")
def circle_path(cx, cy, r):
    return f"M {cx-r:.3f},{cy:.3f} a {r},{r} 0 1,0 {2*r},0 a {r},{r} 0 1,0 {-2*r},0 Z"
def rect(cx, cy, A, x0, x1, y0, y1):
    return path([bay(cx, cy, A, x0, y0), bay(cx, cy, A, x0, y1),
                 bay(cx, cy, A, x1, y1), bay(cx, cy, A, x1, y0)])

def removed(cx, cy):
    """Every piece the router takes out, as separate overlapping rectangles."""
    out = [circle_path(cx, cy, R_HOLE)]
    for b in BAYS:
        out.append(rect(cx, cy, b["A"], -b["notch"], b["notch"], 0.0, COV_Y1))
        for xh, y0, y1 in b["pocket"]:
            out.append(rect(cx, cy, b["A"], -xh, xh, y0, y1))
    out.append(rect(cx, cy, BAT_A, -BAT_HALF, BAT_HALF, BAT_Y0, BAT_Y1))
    return out

def template(cx, cy):
    """Each aperture grown by TOFF — what gets laser-cut in the acrylic."""
    out = []
    for b in BAYS:
        out.append(rect(cx, cy, b["A"], -b["notch"] - TOFF, b["notch"] + TOFF, 45.0, COV_Y1 + TOFF))
        for xh, y0, y1 in b["pocket"]:
            out.append(rect(cx, cy, b["A"], -xh - TOFF, xh + TOFF, y0 - TOFF, y1 + TOFF))
    out.append(rect(cx, cy, BAT_A, -BAT_HALF - TOFF, BAT_HALF + TOFF, BAT_Y0 - TOFF, BAT_Y1 + TOFF))
    return out


class Sheet:
    def __init__(self, w, h): self.w, self.h, self.o, self.defs = w, h, [], []
    def add(self, s): self.o.append(s)
    def define(self, s): self.defs.append(s)
    def text(self, x, y, s, size=4.2, fill=INK, anchor="middle", weight="400", ls="0"):
        s = str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.add(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{fill}" '
                 f'text-anchor="{anchor}" font-weight="{weight}" letter-spacing="{ls}" '
                 f'font-family="Helvetica Neue,Helvetica,Arial,sans-serif">{s}</text>')
    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}mm" height="{self.h}mm" '
                f'viewBox="0 0 {self.w} {self.h}">\n<rect width="{self.w}" height="{self.h}" fill="#fff"/>\n'
                f'<defs>\n' + "\n".join(self.defs) + '\n</defs>\n' + "\n".join(self.o) + "\n</svg>\n")


def draw_frame(sh, cx, cy, uid):
    cuts = removed(cx, cy)
    sh.define(f'<mask id="w{uid}"><path d="{circle_path(cx,cy,R_OUT)}" fill="#fff"/>'
              + "".join(f'<path d="{d}" fill="#000"/>' for d in cuts) + '</mask>')
    sh.add(f'<path d="{circle_path(cx,cy,R_OUT)}" fill="{MAPLE}" mask="url(#w{uid})"/>')
    sh.add(f'<g mask="url(#w{uid})" fill="none" stroke="{INK}" stroke-width="1.0">')
    for d in cuts + [circle_path(cx, cy, R_OUT)]:
        sh.add(f'<path d="{d}"/>')
    sh.add('</g>')
    sh.add(f'<path d="{circle_path(cx,cy,R_RIM_IN)}" fill="none" stroke="{GREY}" '
           f'stroke-width="0.3" stroke-dasharray="3,2"/>')
    sh.define(f'<clipPath id="t{uid}"><path d="{circle_path(cx,cy,R_OUT)} '
              f'{circle_path(cx,cy,R_HOLE-1)}" clip-rule="evenodd"/></clipPath>')
    sh.add(f'<g clip-path="url(#t{uid})">')
    for d in template(cx, cy):
        sh.add(f'<path d="{d}" fill="none" stroke="{MAG}" stroke-width="0.55" stroke-dasharray="3.5,2"/>')
    sh.add('</g>')

    for b in BAYS:                                   # flat cover, one plate
        sh.add(f'<path d="{rect(cx,cy,b["A"],-b["cover"],b["cover"],COV_Y0,COV_Y1)}" '
               f'fill="#2a2a2a" stroke="{INK}" stroke-width="0.4"/>')
        for s in (-1, 1):                            # solid ear + its insert
            x, y = bay(cx, cy, b["A"], s * b["ear"], COV_Y1 + 5)
            sh.add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.0" fill="none" stroke="{GREEN}" stroke-width="1.0"/>')
            a, bb = bay(cx, cy, b["A"], s * b["ear"], COV_Y0), bay(cx, cy, b["A"], s * b["ear"], COV_Y1 + 9)
            sh.add(f'<path d="M {a[0]:.2f},{a[1]:.2f} L {bb[0]:.2f},{bb[1]:.2f}" stroke="{GREEN}" '
                   f'stroke-width="0.5" stroke-dasharray="2,1.4"/>')
        for bx in b["buttons"]:
            x, y = bay(cx, cy, b["A"], bx, (COV_Y0 + COV_Y1) / 2)
            sh.add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.0" fill="{BLUE}" fill-opacity="0.45" '
                   f'stroke="{BLUE}" stroke-width="0.7"/>')
        if b["switch"] is not None:
            sh.add(f'<path d="{rect(cx,cy,b["A"],b["switch"]-5,b["switch"]+5,COV_Y0+0.3,COV_Y1-0.3)}" '
                   f'fill="{BLUE}" fill-opacity="0.5" stroke="{BLUE}" stroke-width="0.6"/>')
    for bi, lbl, x0, x1, y0, y1, port in BOARDS:
        A = BAYS[bi]["A"]; col = RED if port else "#7a5c2e"
        sh.add(f'<path d="{rect(cx,cy,A,x0,x1,y0,y1)}" fill="{col}" fill-opacity="0.24" '
               f'stroke="{col}" stroke-width="0.7"/>')
        if port:
            a, bb = bay(cx, cy, A, (x0 + x1) / 2 - 4.5, COV_Y1), bay(cx, cy, A, (x0 + x1) / 2 + 4.5, COV_Y1)
            sh.add(f'<path d="M {a[0]:.2f},{a[1]:.2f} L {bb[0]:.2f},{bb[1]:.2f}" stroke="{RED}" stroke-width="2.4"/>')
    sh.add(f'<path d="{rect(cx,cy,BAT_A,-40,40,70,91)}" fill="{GREEN}" fill-opacity="0.20" '
           f'stroke="{GREEN}" stroke-width="0.7"/>')
    for W in WEDGES:
        for r, c, dash in ((R_INS_F, BLUE, None), (R_INS_B, RED, "2,1.6")):
            x, y = pol(cx, cy, r, W)
            e = f' stroke-dasharray="{dash}"' if dash else ''
            sh.add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{INSERT_OD/2}" fill="{c}" fill-opacity="0.15" '
                   f'stroke="{c}" stroke-width="0.9"{e}/>')
            sh.add(f'<path d="M {x-5:.2f},{y:.2f} H {x+5:.2f} M {x:.2f},{y-5:.2f} V {y+5:.2f}" '
                   f'stroke="{c}" stroke-width="0.4"/>')


FCX, FCY = 215.0, 312.0


def zoom(sh, uid, bx0, by0, bx1, by1, A, xr, y0, y1, title, sub, pad=14.0):
    pts = [bay(FCX, FCY, A, x, y) for x in (-xr, xr) for y in (y0, y1)]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    cxr, cyr = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    k = min((bx1 - bx0 - pad) / (max(xs) - min(xs)), (by1 - by0 - pad) / (max(ys) - min(ys)))
    DX, DY = (bx0 + bx1) / 2, (by0 + by1) / 2
    sh.define(f'<clipPath id="c{uid}"><rect x="{bx0}" y="{by0}" width="{bx1-bx0}" height="{by1-by0}" rx="2"/></clipPath>')
    sh.add(f'<g clip-path="url(#c{uid})"><rect x="{bx0}" y="{by0}" width="{bx1-bx0}" height="{by1-by0}" '
           f'fill="#fcfcfc"/><g transform="translate({DX:.3f},{DY:.3f}) scale({k:.4f}) '
           f'translate({-cxr:.3f},{-cyr:.3f})">')
    draw_frame(sh, FCX, FCY, uid)
    sh.add('</g></g>')
    sh.add(f'<rect x="{bx0}" y="{by0}" width="{bx1-bx0}" height="{by1-by0}" rx="2" fill="none" '
           f'stroke="{GREY}" stroke-width="0.5"/>')
    sh.text((bx0 + bx1) / 2, by0 - 7.5, title, 5.6, INK, weight="700", ls="1.2")
    sh.text((bx0 + bx1) / 2, by0 - 2.6, sub, 3.4, "#555")
    def at(x, y):
        px, py = bay(FCX, FCY, A, x, y)
        return (DX + k * (px - cxr), DY + k * (py - cyr))
    return at


def main():
    sh = Sheet(880, 742)
    sh.add('<rect x="0" y="0" width="880" height="44" fill="#15202b"/>')
    sh.text(26, 21, "TRON IDENTITY DISC — LOWER FRAME, REV 3", 11.0, "#fff", anchor="start", weight="700", ls="2.0")
    sh.text(26, 32, "FLAT covers · component-sized pockets · routed to a laser-cut acrylic template "
            "· 5/16\" bushing + 1/8\" bit · 1:1", 4.3, "#8fb6d6", anchor="start")
    sh.add('<rect x="700" y="9" width="156" height="26" rx="3" fill="#b5179e"/>')
    sh.text(778, 20, "DRAFT", 11.0, "#fff", weight="700", ls="3")
    sh.text(778, 30, "not for cutting", 3.4, "#ffd9f3")

    draw_frame(sh, FCX, FCY, "F")
    sh.text(FCX, FCY, "HAND HOLE", 4.4, "#9a9a9a", weight="700", ls="1.2")
    sh.text(FCX, FCY + 6, "Ø120", 4.0, "#9a9a9a")
    sh.text(FCX, FCY - 158, "FRONT VIEW", 7.0, INK, weight="700", ls="1.6")
    sh.text(FCX, FCY - 150.5, "seen from the front · angles clockwise from 12 o'clock", 3.7, "#555")
    for phi in range(0, 360, 30):
        a, b = pol(FCX, FCY, R_OUT + 2.5, phi), pol(FCX, FCY, R_OUT + (7 if phi % 60 == 0 else 4.5), phi)
        sh.add(f'<path d="M {a[0]:.2f},{a[1]:.2f} L {b[0]:.2f},{b[1]:.2f}" stroke="{GREY}" '
               f'stroke-width="{0.6 if phi%60==0 else 0.3}"/>')
        if phi % 60 == 0:
            x, y = pol(FCX, FCY, R_OUT + 13, phi); sh.text(x, y + 1.4, f"{phi}°", 3.6, GREY)
    for A, nm in ((60, "BUTTONS"), (300, "ELECTRONICS"), (180, "BATTERY")):
        x, y = pol(FCX, FCY, 104, A); sh.text(x, y, nm, 3.9, "#6b5a36", weight="700")
    for W in WEDGES:
        x, y = pol(FCX, FCY, R_INS_F - 11, W); sh.text(x, y + 1.3, "R102", 3.6, BLUE, weight="700")
        x, y = pol(FCX, FCY, R_INS_B - 10, W); sh.text(x, y + 1.3, "R80", 3.4, RED, weight="700")
        x, y = pol(FCX, FCY, 121, W); sh.text(x, y, f"WEDGE {W:.0f}°", 3.4, "#6b5a36", weight="700")

    at = zoom(sh, "B", 430, 92, 858, 302, 60.0, 42.0, 58.0, 88.0,
              "DETAIL — BUTTONS BAY   (flat cover)",
              "cover 70 × 23.5 × 3 flat, seats on a 14 mm shoulder at y = 64 · 4 buttons at 11 mm pitch · pocket |x| ≤ 21")
    for bx in (-16.5, -5.5, 5.5, 16.5):
        x, y = at(bx, 54); sh.text(x, y, f"{bx:+.1f}", 3.4, BLUE, weight="700")
    x, y = at(0, 50); sh.text(x, y, "tips 1.25–3.32 mm behind the hole edge", 3.4, BLUE, weight="700")
    x, y = at(0, 76); sh.text(x, y, "BOARD 38 × 20 on edge", 3.5, "#444", weight="700")
    x, y = at(0, 87); sh.text(x, y, "pocket |x| ≤ 21, y 64–84, corner R86.6", 3.1, "#666")
    for s in (-1, 1):
        x, y = at(s * 40, 70); sh.text(x, y, "M4 Ø6 insert", 3.3, GREEN, weight="700")
        x, y = at(s * 40, 74); sh.text(x, y, "14 mm shoulder", 2.9, GREEN)

    at = zoom(sh, "E", 430, 352, 858, 572, 300.0, 46.0, 58.0, 102.0,
              "DETAIL — ELECTRONICS BAY   (flat cover)",
              "cover 76 × 23.5 × 3 flat, seats on a 14 mm shoulder at y = 64 · both USB-C mouths square to the cover")
    for lbl, xm, yl in (("ESP32-C3", -13.0, 76.0), ("TP4056", 9.5, 86.0)):
        x, y = at(xm, yl); sh.text(x, y, lbl, 3.6, RED, weight="700")
        x, y = at(xm, 54); sh.text(x, y, "USB-C", 3.3, RED, weight="700")
    x, y = at(0, 58); sh.text(x, y, "slide switch moved out of this cover", 3.1, RED, weight="700")
    x, y = at(-6, 97); sh.text(x, y, "MT3608 stacks on standoffs over the TP4056", 3.3, "#7a5c2e", weight="700")
    x, y = at(-6, 101); sh.text(x, y, "z: 5 + 8 standoff + 8 = 21 of 24 mm", 3.0, "#777")
    for s in (-1, 1):
        x, y = at(s * 44, 72); sh.text(x, y, "M4 Ø6 insert", 3.3, GREEN, weight="700")

    ly = 596
    sh.text(26, ly, "KEY", 4.8, INK, anchor="start", weight="700", ls="1.4")
    for i, (f, s, t) in enumerate((
            (MAPLE, INK, "Solid plywood"), (CUT, INK, "Routed away"),
            ("#2a2a2a", INK, "FLAT 3 mm black acrylic cover"),
            ("#ffffff", MAG, "TEMPLATE aperture = finished pocket + 2.3813"),
            (RED, RED, "Board with USB-C; bar at y = 64 is the port mouth"),
            (BLUE, BLUE, "Button tip / slide switch"),
            (GREEN, GREEN, "18650 holder · M4 insert in the solid ear"))):
        y = ly + 8 + i * 7.2
        sh.add(f'<rect x="26" y="{y-4.0}" width="6.5" height="5.4" fill="{f}" stroke="{s}" stroke-width="0.6"/>')
        sh.text(36, y, t, 3.5, "#333", anchor="start")

    nx = 320
    sh.text(nx, ly, "REV 3 — FLAT COVERS", 4.8, INK, anchor="start", weight="700", ls="1.2")
    notes = [
        ("Flat, and it still hugs the hole — because the covers are short.", GREEN,
         "A flat plate only runs away from a round hole if it is long. Rev 1's was 106 mm and finished 32.9 mm back.",
         "Setback at everything you actually touch: buttons 1.3 and 3.8 mm, TP4056 port 1.7, ESP32 port 2.4, slide",
         "switch 6.0. The cover ends sit further back but you never reach there — they are the screw ears."),
        ("The ear rebate had to go — it could not be routed.", MAG,
         "A 3 mm-deep rebate needs a 7.76 mm template aperture and your bushing is 7.938: it would not fit. So the",
         "notch is now the full cover width and the cover seats on the shoulder where the narrower pocket behind it",
         "steps in — 6.41 mm of bearing each side after the R1.5875 fillet. Inserts drill into that shoulder face."),
        ("What the flat cover costs.", RED,
         "The 80 mm protoboard is out; a flat notch that wide puts its ends 25.8 mm back. Button board is now",
         "38 × 20 with the four switches at 11 mm pitch. And the MT3608 no longer fits beside the other two boards,",
         "so it stacks on standoffs over the TP4056 — 21 mm of the 24 mm bay height. Both need your OK."),
        ("Router-ready.", MAG,
         "Magenta is the acrylic template: every aperture grown by 2.3813 for the 5/16\" bushing. Inside corners",
         "finish at R1.5875 by design. No blocks anywhere, so nothing to chisel and nothing to glue — the cover",
         "screws go into Ø6 M4 inserts drilled radially into the 14 mm shoulders at x = ±28 and ±31."),
        ("Two defects found by auditing, not by eye.", RED,
         "(a) The cover inserts did not fit. An 8 mm shoulder leaves 0–1 mm of wood round a Ø6–Ø8 bore.",
         "Shoulders are now 14 mm: buttons pocket |x| ≤ 21 with the pitch tightened to 11 mm, electronics",
         "pocket |x| ≤ 24 with the slide switch moved out of the cover. Ø6 inserts, 4 mm of wood each side.",
         "(b) A 1/8in bit cannot reach 24 mm of ply plus the template — it needs 27–30 mm of stickout and",
         "will snap. The template can only establish the top of the wall; the depth has to be finished with",
         "a bearing-guided flush-trim bit, which also changes the finished corner radius. See note below."),
        ("Still unanswered.", RED,
         "WHICH FLUSH-TRIM BIT? 1/4in gives R3.175 corners, 1/2in gives R6.350 — not the R1.5875 drawn here.",
         "One routed 24 mm sheet or four glued 6 mm layers? Bays through-cut or blind? MOSFET board dimensions.",
         "Battery pocket corners reach R100.7 — a rigid cell has to be a chord, so it is the one thing outside R95."),
    ]
    y = ly + 8
    for head, col, *body in notes:
        sh.text(nx, y, head, 3.8, col, anchor="start", weight="700"); y += 4.3
        for ln in body:
            sh.text(nx, y, ln, 3.3, "#444", anchor="start"); y += 3.9
        y += 2.2

    sh.add('<rect x="0" y="732" width="880" height="10" fill="#15202b"/>')
    sh.text(26, 738.6, "build-plans/render/frame_render_v3.py  ·  python3 frame_render_v3.py && "
            "rsvg-convert -w 2600 frame-plan-v3.svg -o frame-plan-v3.png", 3.3, "#8fb6d6", anchor="start")
    open("frame-plan-v3.svg", "w").write(sh.svg())
    print("wrote frame-plan-v3.svg")


if __name__ == "__main__":
    main()

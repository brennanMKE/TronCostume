#!/usr/bin/env python3
"""Electronics carrier — a TWO-LAYER structural mount, no board hardware needed.

Layer A, base: the plain sector.
Layer B, pocket plate: the same sector with a press-fit pocket per board, cemented
on top of A. Each board drops into its pocket and is located on all four sides by
3 mm of acrylic — it cannot shift, rotate or creep. Small retainer tabs cement over
the board edges afterwards to stop it lifting.

This replaces cable ties, which located nothing.
"""
import math, os

A = 300.0
R_IN, R_OUT, BR_HALF = 72.0, 108.0, 14.0
SHEET, C = 260.0, 130.0
FIT = 0.2                      # pocket clearance; laser kerf makes this a snug push fit
USB_W, USB_D = 10.0, 5.0       # notch so the connector body clears the pocket wall

BOARDS = [
    ("ESP32-C3",  -43.0, -25.0, 74.0,  96.5, True),
    ("TP4056",    -16.0,   1.0, 78.0, 106.0, True),
    ("MT3608",     13.0,  45.8, 77.0,  94.8, False),
]
MOUNT = ((-30.0, 100.0), (30.0, 98.0), (-20.5, 76.5), (7.0, 76.5))


def bp(x, y, a=A):
    r = math.radians(a)
    return (C + y * math.sin(r) + x * math.cos(r), C - y * math.cos(r) + x * math.sin(r))

def pol(r, phi):
    a = math.radians(phi); return (C + r * math.sin(a), C - r * math.cos(a))

def arc(r, a0, a1, step=0.5):
    n = max(2, int(abs(a1 - a0) / step))
    return [pol(r, a0 + (a1 - a0) * i / n) for i in range(n + 1)]

def P(pts, close=True):
    return "M " + " L ".join(f"{x:.4f},{y:.4f}" for x, y in pts) + (" Z" if close else "")

def rect(x0, x1, y0, y1):
    return P([bp(x0, y0), bp(x0, y1), bp(x1, y1), bp(x1, y0)])

def circ(x, y, d):
    px, py = bp(x, y); r = d / 2
    return f"M {px-r:.4f},{py:.4f} a {r},{r} 0 1,0 {2*r},0 a {r},{r} 0 1,0 {-2*r},0 Z"

def plate():
    def e(r): return math.degrees(math.asin(min(1.0, BR_HALF / r)))
    return P(arc(R_IN, A - 60 + e(R_IN), A + 60 - e(R_IN))
             + list(reversed(arc(R_OUT, A - 60 + e(R_OUT), A + 60 - e(R_OUT)))))

def inside(x, y):
    px, py = bp(x, y); X, Y = px - C, C - py
    r = math.hypot(X, Y)
    if not (R_IN <= r <= R_OUT): return False
    phi = math.degrees(math.atan2(X, Y)) % 360
    d = (phi - A + 180) % 360 - 180
    return abs(d) <= 60.0 - math.degrees(math.asin(min(1.0, BR_HALF / r)))

def pocket(x0, x1, y0, y1, port):
    """board pocket, with a notch at the USB end so the connector clears the wall"""
    a, b = x0 - FIT/2, x1 + FIT/2
    c, d = y0 - FIT/2, y1 + FIT/2
    if not port:
        return [rect(a, b, c, d)]
    m = (x0 + x1) / 2
    return [P([bp(a, c), bp(a, d), bp(b, d), bp(b, c),
               bp(m + USB_W/2, c), bp(m + USB_W/2, c - USB_D),
               bp(m - USB_W/2, c - USB_D), bp(m - USB_W/2, c)])]

def label(out, x, y, txt, size=3.4):
    tx, ty = bp(x, y)
    out.append(f'<text x="{tx:.2f}" y="{ty:.2f}" font-size="{size}" fill="#0000ff" '
               f'text-anchor="middle" font-family="Helvetica" '
               f'transform="rotate({A-360:.1f} {tx:.2f} {ty:.2f})">{txt}</text>')

def emit(name, title, desc, cut, eng=(), extra_text=()):
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{SHEET}mm" height="{SHEET}mm" '
           f'viewBox="0 0 {SHEET} {SHEET}">', f'<title>{title}</title><desc>{desc}</desc>',
           '<g id="engrave" fill="none" stroke="#0000ff" stroke-width="0.1">']
    out += [f'<path d="{d}"/>' for d in eng]
    out += list(extra_text)
    out += ['</g>', '<g id="cut" fill="none" stroke="#000000" stroke-width="0.1">']
    out += [f'<path d="{d}"/>' for d in cut]
    out += ['</g>', '</svg>', '']
    os.makedirs("v4", exist_ok=True)
    open(os.path.join("v4", name), "w").write("\n".join(out))
    print("  ", name)


print("checks:")
bad = 0
def pocket_pts(x0, x1, y0, y1, port):
    """the actual outline vertices, not a bounding box"""
    a, b = x0 - FIT/2, x1 + FIT/2
    c, d = y0 - FIT/2, y1 + FIT/2
    if not port:
        return [(a, c), (a, d), (b, d), (b, c)]
    m = (x0 + x1) / 2
    return [(a, c), (a, d), (b, d), (b, c),
            (m + USB_W/2, c), (m + USB_W/2, c - USB_D),
            (m - USB_W/2, c - USB_D), (m - USB_W/2, c)]

for lbl, x0, x1, y0, y1, port in BOARDS:
    pts = pocket_pts(x0, x1, y0, y1, port)
    ok = all(inside(x, y) for x, y in pts)
    print(f"   {lbl:10} pocket {x1-x0+FIT:5.1f} x {y1-y0+FIT:5.1f}  "
          f"max R{max(math.hypot(x,y) for x,y in pts):6.1f}  {'OK' if ok else 'OFF THE PLATE'}")
    bad += 0 if ok else 1
for mx, my in MOUNT:
    if not inside(mx, my): print(f"   mount {mx},{my} OFF THE PLATE"); bad += 1
# pocket walls must not get too thin between neighbours
pairs = [(BOARDS[0], BOARDS[1]), (BOARDS[1], BOARDS[2])]
for a_, b_ in pairs:
    gap = (b_[1] - FIT/2) - (a_[2] + FIT/2)
    print(f"   wall between {a_[0]} and {b_[0]}: {gap:5.1f} mm   {'OK' if gap >= 6 else 'THIN'}")
    bad += 0 if gap >= 6 else 1
print("   FAIL" if bad else "   all good")

# ---- layer A: base
emit("12a-carrier-base-3mm.svg", "Carrier BASE — acrylic 3 mm",
     "Cut. Plain sector R72-R108. Layer B cements on top of this. Four 3.5 holes screw the "
     "pair to the back carrier.",
     [plate()] + [circ(x, y, 3.5) for x, y in MOUNT])

# ---- layer B: pocket plate
cutB = [plate()] + [circ(x, y, 3.5) for x, y in MOUNT]
engB, txtB = [], []
for lbl, x0, x1, y0, y1, port in BOARDS:
    cutB += pocket(x0, x1, y0, y1, port)
    label(txtB, (x0 + x1) / 2, (y0 + y1) / 2, lbl, 3.6)
    if port:
        label(txtB, (x0 + x1) / 2, y0 - 7.5, "USB-C", 3.0)
emit("12b-carrier-pockets-3mm.svg", "Carrier POCKET PLATE — acrylic 3 mm",
     "Cut. Same sector as 12a with a press-fit pocket for each board. Cement on top of 12a. "
     "Each board drops into its pocket and is located on all four sides by 3 mm of acrylic. "
     "Pockets are board size + 0.2; laser kerf makes that a snug push fit. The notch at each "
     "USB end clears the connector body.",
     cutB, [], txtB)

# ---- retainer tabs, cut on their own small sheet
tabs, tx0 = [], 20.0
for i in range(8):
    x = tx0 + (i % 4) * 16.0
    y = 20.0 + (i // 4) * 12.0
    tabs.append(f"M {x:.2f},{y:.2f} h 12 v 7 h -12 Z")
    tabs.append(f"M {x+3:.2f},{y+3.5:.2f} a 1.6,1.6 0 1,0 3.2,0 a 1.6,1.6 0 1,0 -3.2,0 Z")
emit("12c-carrier-retainers-3mm.svg", "Carrier RETAINERS — acrylic 3 mm, 8 off",
     "Cut 8. After a board is in its pocket, cement a tab across the pocket wall so it "
     "overhangs the board edge by about 2 mm. Two per board stops it lifting out. The 3.2 "
     "hole is optional, for an M3 screw instead of cement.",
     tabs)
print("\nwrote the three carrier layers")

#!/usr/bin/env python3
"""Electronics carrier plate — 3 mm acrylic, sits in the 300 deg bay.

Both USB-C ports face the same way, at the inner edge. No board needs mounting
holes: every one is held by a cable tie through a pair of slots, plus foam tape.
MT3608 measured from Brennan's photo: 32.8 x 17.8, no mounting holes.
"""
import math

A = 300.0                      # electronics bay centre
R_IN, R_OUT, BR_HALF = 72.0, 108.0, 14.0   # plate: bay inset 2 mm off each bridge
SHEET = 260.0
C = SHEET / 2
TIE_W, TIE_L = 1.8, 14.0       # cable-tie slot

BOARDS = [
    # label,        x0,    x1,   y0,    y1,   port?
    ("ESP32-C3",  -43.0, -25.0, 74.0,  96.5, True),
    ("TP4056",    -16.0,   1.0, 74.0, 102.0, True),
    ("MT3608",     13.0,  45.8, 77.0,  94.8, False),
]


def bp(x, y, a=A):
    r = math.radians(a)
    return (C + y * math.sin(r) + x * math.cos(r), C - y * math.cos(r) + x * math.sin(r))


def pol(r, phi):
    a = math.radians(phi)
    return (C + r * math.sin(a), C - r * math.cos(a))


def arc(r, a0, a1, step=0.5):
    n = max(2, int(abs(a1 - a0) / step))
    return [pol(r, a0 + (a1 - a0) * i / n) for i in range(n + 1)]


def P(pts, close=True):
    return "M " + " L ".join(f"{x:.4f},{y:.4f}" for x, y in pts) + (" Z" if close else "")


def rect(x0, x1, y0, y1):
    return P([bp(x0, y0), bp(x0, y1), bp(x1, y1), bp(x1, y0)])


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


cut, eng = [plate()], []
for mx, my in ((-30.0, 100.0), (30.0, 98.0), (-20.5, 76.5), (7.0, 76.5)):      # plate mounting holes
    px, py = bp(mx, my)
    cut.append(f"M {px-1.75:.4f},{py:.4f} a 1.75,1.75 0 1,0 3.5,0 a 1.75,1.75 0 1,0 -3.5,0 Z")
for lbl, x0, x1, y0, y1, port in BOARDS:
    eng.append(rect(x0, x1, y0, y1))
    my = (y0 + y1) / 2
    for xx in (x0 - 2.6, x1 + 2.6):                 # a tie slot either side of each board
        cut.append(rect(xx - TIE_W / 2, xx + TIE_W / 2, my - TIE_L / 2, my + TIE_L / 2))
    if port:                                         # mark the USB-C mouth on the engrave layer
        eng.append(rect((x0 + x1) / 2 - 4.5, (x0 + x1) / 2 + 4.5, y0 - 1.2, y0))

for mx, my in ((-30.0, 100.0), (30.0, 98.0), (-20.5, 76.5), (7.0, 76.5)):
    assert inside(mx, my), f"mounting hole {mx},{my} is off the plate"
print("corner check — every board and slot inside the plate:")
bad = 0
for lbl, x0, x1, y0, y1, port in BOARDS:
    pts = [(x, y) for x in (x0 - 2.6 - TIE_W/2, x1 + 2.6 + TIE_W/2) for y in (y0, y1)]
    ok = all(inside(x, y) for x, y in pts)
    r0 = max(math.hypot(x, y) for x, y in pts)
    print(f"  {lbl:10} {x1-x0:5.1f} x {y1-y0:5.1f}   far corner R{r0:6.1f}   {'OK' if ok else 'OUTSIDE'}")
    bad += 0 if ok else 1
print(f"  plate spans R{R_IN:.0f}-R{R_OUT:.0f}; bay is R72-R110 so 2 mm clear at the rim")
print("  FAIL" if bad else "  all inside")

out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{SHEET}mm" height="{SHEET}mm" '
       f'viewBox="0 0 {SHEET} {SHEET}">',
       '<title>Electronics carrier plate - 3 mm acrylic</title>',
       '<desc>CUT black: plate outline and cable-tie slots. ENGRAVE blue: board outlines, '
       'USB-C mouths and labels - do not cut. Both USB-C ports face the inner edge. No board '
       'needs mounting holes; each is held by one cable tie through its pair of slots plus '
       'foam tape. MT3608 measured 32.8 x 17.8 from the supplied photo.</desc>',
       '<g id="engrave" fill="none" stroke="#0000ff" stroke-width="0.1">']
out += [f'<path d="{d}"/>' for d in eng]
for lbl, x0, x1, y0, y1, port in BOARDS:
    tx, ty = bp((x0 + x1) / 2, (y0 + y1) / 2)
    ang = A - 360.0
    out.append(f'<text x="{tx:.2f}" y="{ty:.2f}" font-size="4" fill="#0000ff" '
               f'text-anchor="middle" font-family="Helvetica" '
               f'transform="rotate({ang:.1f} {tx:.2f} {ty:.2f})">{lbl}</text>')
for lbl, x0, x1, y0, y1, port in BOARDS:
    if not port: continue
    tx, ty = bp((x0 + x1) / 2, y0 - 3.4)
    out.append(f'<text x="{tx:.2f}" y="{ty:.2f}" font-size="3.2" fill="#0000ff" '
               f'text-anchor="middle" font-family="Helvetica" '
               f'transform="rotate({A-360:.1f} {tx:.2f} {ty:.2f})">USB-C</text>')
out += ['</g>', '<g id="cut" fill="none" stroke="#000000" stroke-width="0.1">']
out += [f'<path d="{d}"/>' for d in cut]
out += ['</g>', '</svg>', '']
import os
os.makedirs("v4", exist_ok=True)
open("v4/12-electronics-carrier-plate-3mm.svg", "w").write("\n".join(out))
print("\nwrote v4/12-electronics-carrier-plate-3mm.svg")

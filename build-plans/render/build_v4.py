#!/usr/bin/env python3
"""Tron disc v4 — every cut file, generated from one set of constants.

Stack, z from the front:
  0– 3  top plate      3 mm acrylic: black + white C inset + white outer ring
  3–12  channel layer  9 mm ply, both LED channels
 12–15  divider        3 mm ply, full annulus — this is what makes it a box
 15–39  frame         24 mm ply, three bridges, three open bays (the router job)
 39–42  carrier/back   3 mm acrylic, every component mounts to it
"""
import math, os

IN = 25.4
BUSH, BIT = 5 / 16 * IN, 1 / 8 * IN
OFF = (BUSH - BIT) / 2                      # 2.38125 template offset

R_HOLE, R_OUT = 60.0, 130.0
RIM_IN, RIM_OUT = 60.0, 72.0                # inner rim
BAY_IN, BAY_OUT = 72.0, 110.0               # open bay
BR_HALF = 12.0                              # bridges 24 wide
BRIDGES = (0.0, 120.0, 240.0)
# bay centre angle -> inner radius. Buttons and electronics run straight into the hand
# hole so the switches and both USB-C ports are reachable with no wall in the way. The
# battery bay keeps the inner rim, because that is where your hand grips.
BAY = {"BUTTONS": (60.0, 50.0), "BATTERY": (180.0, 72.0), "ELECTRONICS": (300.0, 50.0)}

C_IN, C_OUT, C_GAP = 82.0, 88.0, 20.0       # white C in the top plate
RING_IN = 118.0                             # white outer ring R118–130
CH_C = (79.0, 91.0)                         # C channel in the 9 mm layer
CH_O = (117.0, 127.0)                       # outer channel
SCREW_F, SCREW_B = 96.0, 80.0               # M4 front / back circles

BTN_X = (-27.0, -9.0, 9.0, 27.0)
BTN_NOTCH, USB_NOTCH = 35.0, 23.0           # half-widths of the inner-rim notches
WIRE_R = 90.0                               # Ø8 hole through each bridge

SHEET = 300.0
C0 = SHEET / 2


def pol(r, phi, cx=C0, cy=C0):
    a = math.radians(phi)
    return (cx + r * math.sin(a), cy - r * math.cos(a))


def bp(A, x, y):
    a = math.radians(A)
    return (C0 + y * math.sin(a) + x * math.cos(a), C0 - y * math.cos(a) + x * math.sin(a))


def arc(r, a0, a1, step=0.5):
    n = max(2, int(abs(a1 - a0) / step))
    return [pol(r, a0 + (a1 - a0) * i / n) for i in range(n + 1)]


def P(pts, close=True):
    return "M " + " L ".join(f"{x:.4f},{y:.4f}" for x, y in pts) + (" Z" if close else "")


def circle(r, cx=C0, cy=C0):
    return (f"M {cx-r:.4f},{cy:.4f} a {r:.4f},{r:.4f} 0 1,0 {2*r:.4f},0 "
            f"a {r:.4f},{r:.4f} 0 1,0 {-2*r:.4f},0 Z")


def ring(r0, r1):
    return circle(r0) + " " + circle(r1)


def c_slot(r0=C_IN, r1=C_OUT):
    a0, a1 = C_GAP / 2, 360 - C_GAP / 2
    return P(arc(r1, a0, a1) + list(reversed(arc(r0, a0, a1))))


def bay_path(A, r_in, r_out, half):
    """Open sector between the two bridges either side of bay centre A."""
    def edge(r):                                    # angular offset of a bridge edge
        return math.degrees(math.asin(min(1.0, half / r)))
    b0, b1 = A - 60.0, A + 60.0
    return P(arc(r_in, b0 + edge(r_in), b1 - edge(r_in))
             + list(reversed(arc(r_out, b0 + edge(r_out), b1 - edge(r_out)))))


def notch(A, half, r0=RIM_IN - 4, r1=RIM_OUT):
    return P([bp(A, -half, r0), bp(A, -half, r1), bp(A, half, r1), bp(A, half, r0)])


def hole(r, phi, d):
    x, y = pol(r, phi)
    return circle(d / 2, x, y)


def slot(A, x0, x1, y0, y1):
    return P([bp(A, x0, y0), bp(A, x0, y1), bp(A, x1, y1), bp(A, x1, y0)])


def emit(name, title, desc, cut, engrave=()):
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{SHEET}mm" height="{SHEET}mm" '
           f'viewBox="0 0 {SHEET} {SHEET}">', f'<title>{title}</title><desc>{desc}</desc>']
    if engrave:
        out.append('<g id="engrave" fill="none" stroke="#0000ff" stroke-width="0.1">')
        out += [f'<path d="{d}"/>' for d in engrave]
        out.append('</g>')
    out.append('<g id="cut" fill="none" stroke="#000000" stroke-width="0.1">')
    out += [f'<path d="{d}"/>' for d in cut]
    out += ['</g>', '</svg>', '']
    os.makedirs("v4", exist_ok=True)
    open(os.path.join("v4", name), "w").write("\n".join(out))
    print(" ", name)


SCREWS_F = [hole(SCREW_F, b, 4.5) for b in BRIDGES]
SCREWS_B = [hole(SCREW_B, b, 4.5) for b in BRIDGES]
REF = [circle(R_OUT), circle(R_HOLE),
       f"M {C0-8:.3f},{C0:.3f} H {C0+8:.3f} M {C0:.3f},{C0-8:.3f} V {C0+8:.3f}"]

print("writing v4 cut files:")

# 1 — top plate, black acrylic 3 mm
emit("1-top-black-3mm.svg", "Top plate — BLACK acrylic 3 mm",
     "Cut. OD 236 (R118), hole Ø120, C slot R82-88 with a 20 deg bridge at 12 o'clock, "
     "3 x 4.5 countersunk at R96. The white ring butts to its outer edge at R118.",
     [circle(RING_IN), circle(R_HOLE), c_slot()] + SCREWS_F)

# 2 — white C inset
emit("2-top-white-C-3mm.svg", "C inset — WHITE acrylic 3 mm",
     "Cut ONE. Same path as the slot in part 1, so the laser kerf leaves a cement gap.",
     [c_slot()])

# 3 — white outer ring
emit("3-top-white-ring-3mm.svg", "Outer ring — WHITE acrylic 3 mm",
     "Cut. OD 260, ID 236. Butts to the black face at R118 and is solvent-cemented to it.",
     [circle(R_OUT), circle(RING_IN)])

# 4 — channel layer, 9 mm ply
emit("4-channel-9mm-ply.svg", "Channel layer — plywood 9 mm",
     "Cut. Both LED channels go right through: C channel R79-91 (340 deg, solid bridge at "
     "12 o'clock) and outer channel R117-127, full circle. Strips lie flat on the divider "
     "below, facing up.",
     [circle(R_OUT), circle(R_HOLE), c_slot(*CH_C), ring(*CH_O)] + SCREWS_F)

# 5 — divider, 3 mm ply
emit("5-divider-3mm-ply.svg", "Divider — plywood 3 mm",
     "Cut. Full annulus: the floor of both LED channels and the ceiling of the three bays. "
     "This is the part that makes the disc a stiff box. Four 8 mm wire holes.",
     [circle(R_OUT), circle(R_HOLE)] + SCREWS_F
     + [hole(85, a, 8.0) for a in (352, 8)] + [hole(122, a, 8.0) for a in (352, 8)])

# 6 — carrier / back, 3 mm acrylic
carrier = [circle(R_OUT), circle(R_HOLE)] + SCREWS_B
E = BAY["ELECTRONICS"][0]
for x0, x1, y0, y1 in ((-32, -14, 73, 95.5), (-10, 7, 73, 101), (12, 48, 76, 93)):
    cx_, cy_ = (x0 + x1) / 2, (y0 + y1) / 2
    for sx in (x0 + 3.5, x1 - 3.5):
        for sy in (y0 + 3.5, y1 - 3.5):
            p = bp(E, sx, sy); carrier.append(circle(1.6, *p))
carrier.append(slot(BAY["BUTTONS"][0], -41, 41, 71.1, 72.9))          # protoboard drops in on edge
for sx in (-34, 34):                                                # battery holder screws
    p = bp(BAY["BATTERY"][0], sx, 86.5); carrier.append(circle(1.6, *p))
emit("6-carrier-3mm-acrylic.svg", "Carrier / back cover — acrylic 3 mm",
     "Cut. Full annulus OD 260 / ID 120. 3 x 4.5 countersunk at R80 into the frame's back "
     "inserts. 1.8 x 82 slot takes the button protoboard on edge. 3.2 holes are M3 "
     "standoffs for the three boards and the battery holder. Build the whole electronics "
     "pack on this off the disc, then screw it on.",
     carrier)

# 7 — ROUTER TEMPLATE for the 24 mm frame
tpl = [circle(R_HOLE - OFF)]
tpl += [bay_path(a, ri - OFF, BAY_OUT + OFF, BR_HALF - OFF) for a, ri in BAY.values()]
emit("7-router-template-acrylic.svg", "ROUTER TEMPLATE — acrylic, for the 24 mm frame",
     f"Cut. Every aperture is already grown by {OFF:.5f} for a 5/16in OD guide bushing with "
     f"a 1/8in bit — do NOT add compensation in xTool. Cuts the hand hole, the three bays "
     f"and the three bays; the O260 perimeter is file 9. Three 4.5 holes at R96 "
     f"screw it to the blank. Engrave layer is reference only.",
     tpl + SCREWS_F, REF + [circle(SCREW_F), circle(SCREW_B)]
     + [hole(WIRE_R, b, 8.0) for b in BRIDGES])

# 9 — outside guide for the Ø260 perimeter
emit("9-od-guide-disc-acrylic.svg", "OD guide disc — acrylic",
     f"Cut. A disc of {2*(R_OUT-OFF):.2f} mm. Screw it to the blank through the same three "
     f"R96 holes and run the bushing AROUND ITS OUTSIDE: the bit then cuts the Ø260 "
     f"perimeter. The perimeter cannot live in template 7 — as an aperture its guide ring "
     f"would fall away as soon as it was cut.",
     [circle(R_OUT - OFF)] + SCREWS_F)

# 8 — the finished frame, for checking
fin = [circle(R_HOLE), circle(R_OUT)]
fin += [bay_path(a, ri, BAY_OUT, BR_HALF) for a, ri in BAY.values()]
emit("8-frame-finished-REFERENCE.svg", "Frame as finished — REFERENCE, do not cut",
     "What the 24 mm plywood should measure after routing. Routed corners will carry the "
     "flush-trim bit's radius, which this outline does not show.",
     fin, [circle(SCREW_F), circle(SCREW_B)])

# ---- checks
print("\nchecks:")
bad = 0
def inbay(A, x, y):
    """Bridges are rays, not lines: test the angular offset from the bay centre."""
    px, py = bp(A, x, y); X, Y = px - C0, C0 - py
    r = math.hypot(X, Y)
    if not (BAY_IN <= r <= BAY_OUT): return False
    phi = math.degrees(math.atan2(X, Y)) % 360
    d = (phi - A + 180) % 360 - 180
    return abs(d) <= 60.0 - math.degrees(math.asin(min(1.0, BR_HALF / r)))
for nm, A, box in (("ESP32-C3", E, (-32, -14, 73, 95.5)), ("TP4056", E, (-10, 7, 73, 101)),
                   ("MT3608", E, (12, 48, 76, 93)),
                   ("protoboard", BAY["BUTTONS"][0], (-41, 41, 71.5, 72.5)),
                   ("18650 holder", BAY["BATTERY"][0], (-38.5, 38.5, 76, 97))):
    x0, x1, y0, y1 = box
    ok = all(inbay(A, x, y) for x in (x0, x1) for y in (y0, y1))
    print(f"  {nm:14} inside its bay: {'yes' if ok else 'NO'}")
    bad += 0 if ok else 1
ap = [("bay", (BAY_OUT + OFF) - (BAY_IN - OFF))]
for nm, w in ap:
    print(f"  template {nm:12} narrowest {w:6.2f} mm vs {BUSH:.3f} bushing: {'ok' if w >= BUSH else 'TOO NARROW'}")
print(f"  bridge at the template: {2*(BR_HALF-OFF):.2f} mm wide, finished {2*BR_HALF:.0f} mm")
print("  FAIL" if bad else "  all components inside their bays")

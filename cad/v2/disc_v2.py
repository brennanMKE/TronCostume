"""Tron identity disc v2: three-bridge frame, removable back (build123d). All mm.

Stack, bottom to top:
  back      black acrylic 3      z -3..0   buttons, battery window, rear screws
  frame     maple 2 x 5          z  0..10  inner ring, outer ring, 3 bridges, open sectors
  LED       maple 2 x 5          z 10..20  C channel + outer strip wall (same as v1 layers 4-5)
  ring      white acrylic 10     z 10..20  R110-R130
  face + C  black / white 3      z 20..23
  battery   black acrylic box under the back at 6 o'clock
  All electronics (buttons, battery, charger, ESP32-C3, MT3608) mount on the back.

Angles are clockwise from 12 o'clock seen from the front. In a sector's local
frame x is radial and y is tangential. Run with build123d-mcp execute_file().
"""
import math
from build123d import *

OUTER_D, INNER_D = 260.0, 120.0
ACRYLIC_T, PLY_T, WHITE_T = 3.0, 5.0, 10.0
FRAME_N = 3                          # 15 mm: the 12 mm inserts fit inside the frame; holder box sticks out 7.5
FRAME_H = FRAME_N * PLY_T

# frame (concept: three-bridge annular frame)
RING_IN_OUT = 74.0                   # inner ring R60-R74
RING_OUT_IN = 114.0                  # outer ring R114-R130, under the white ring
BRIDGE_W = 20.0
BRIDGES = (0, 120, 240)

# LED layers (unchanged from v1)
C_CH_IN, C_CH_OUT = 80.0, 96.0
WHITE_IN_R = 110.0
STRIP_T, STRIP_W = 3.0, 5.0
WOOD_OUT_R = WHITE_IN_R - STRIP_T    # 107
C_GAP_DEG = 20.0
FACE_OUT_R = 114.0
C_IN_R, C_OUT_R = 82.0, 88.0

# fasteners
SCREW_CLR_D = 4.5                    # M4 clearance
INSERT_D, INSERT_L = 9.9, 12.0       # M4-0.7 x 12 wood insert, 9.9 thread OD
INSERT_HOLE_D = 7.8                  # drawn size; the kerf opens it to about 8.0 - confirm with insert-test-coupon
FRONT_R = 101.0                      # face screws -> inserts in the bridge tops (outer end)
REAR_R = 84.0                        # back screws -> inserts in the bridge bottoms (inner end)
REAR_RING_R, REAR_RING_ANGLES = 122.0, (60, 180, 300)   # extra back screws in the outer ring
WIRE_W, WIRE_R = 5.0, 92.5           # wire notch across bridges 0 and 240 in the BOTTOM frame layer: wires on the back pass under

# buttons: protoboard screwed to the inside of the back, switches facing out
BTN_ANGLE, BTN_R = 60, 90.0          # board center
BOARD_L, BOARD_W, BOARD_T = 80.0, 20.0, 1.6
SW, SW_H, SW_CLR = 6.0, 3.5, 0.2     # 6x6 switch body, its height, hole clearance per side
SW_STANDOFF = 0.0                    # gap between switch body and board - measure
BTN_PITCH = 10.0                     # 36 across four 6 mm switches with 4 mm gaps
BTN_OFF_L, BTN_OFF_W = -3.8, -4.0    # button row center from board center (from the photo - measure)
MOUNT_DX, MOUNT_DY, MOUNT_D = 37.0, 7.5, 2.4   # M2 corner holes (estimated - measure)

# Electronics pod at 10 o'clock: TP4056 charger, MT3608 boost and ESP32-C3 side by side on the back,
# USB-C ports at the hand hole. A thin locator sheet with a pocket per board, then a 3 mm black
# hold-down plate with windows, clamped to the back by small black screws from outside, nuts inside.
# Local frame: x from R61 outward, y sideways, z up from the back's inside face. Sizes from the photos.
USB_ANGLE, USB_NOTCH_W = 300, 59.0
POD_R0 = 63.0                        # pod starts behind the 3 mm face plate (R60-R63)
FP_T, FP_CLR, FP_SLOT_CLR = 3.0, 0.25, 0.3   # face plate: black 3 mm, cemented to the back; port openings +0.3 a side
POD_LOC_T, POD_PLATE_T = 1.0, 3.0    # locator = board thickness (all three boards are 1.0); hold-down in the 3 mm black
POD_X1, POD_HALF_W = 48.6, 27.5      # carrier plates: x 0..48.6; +-27.5 at the front (screws), +-BACK_HALF_W at the back
POD_BACK_R = 6.0
BACK_HALF_W = 20.9
POD_CLR, POD_RIM = 0.2, 0.8          # pocket clearance per side; hold-down rim over each board edge
BOARD_X0 = 0.0                       # board front edges against the face plate; USB-C sticks 1.5 into its openings
USBC_W, USBC_L, USBC_H, USBC_OUT = 8.9, 7.3, 3.2, 1.5   # USB-C receptacle; sticks out 1.5 past the board edge (measured on the ESP32)
PODS = {                             # name: (y0, y1, length, pcb thickness), built pointing outward
    "tp4056": (-19.15, -1.85, 28.0, 1.0),   # measured 28 x 17.3 x 1.0
    "esp32c3": (1.25, 19.25, 22.0, 1.0),    # measured 22 x 18 x 1.0
    "mt3608": (-8.6, 8.6, 37.0, 1.0),       # measured 37 x 17.2 x 1.0; no USB-C: turned sideways behind (see MT_X0)
}
MT_X0 = 29.2                         # MT3608's front edge once turned sideways (x 29.2..46.4, y +-18.5)
POD_SCREWS = [(4.0, -25.0), (4.0, 25.0), (32.0, -25.0), (32.0, 25.0)]   # outside the cover, so they unscrew
POD_SCREW_HOLE, POD_SCREW_L = 2.4, 10.0      # M2 x 10 black, nuts on top of the plate
M2_NUT_AF, M2_NUT_H = 4.0, 1.6
PLUG_W = 12.4                        # USB-C plug overmold, about 12.4 x 6.5

# battery: holder in a black acrylic box under the back
HOLDER_L, HOLDER_W, HOLDER_H = 80.0, 21.0, 22.0
HOLDER_ANGLE, HOLDER_IN = 180, 75.0
HOLDER_CLR = 0.5
BOX_SCREW_D = 3.4                    # holder's single screw, center of the floor (assumed)
# battery box: stacked 3 mm black acrylic, no cement - rings with the holder opening, then a solid floor,
# clamped by four M3 screws up through the stack and the back, nuts inside the disc
BOX_RINGS = 2
BOX_HALF_W, BOX_HALF_L = 21.0, 50.5  # outside 42 x 101, centered on the holder
BOX_SCREWS = [(sx*16.0, sy*42.0) for sx in (-1, 1) for sy in (-1, 1)]   # (across, along) from the holder center
BOX_SCREW_HOLE = 3.4                 # M3 clearance
NUT_AF, NUT_H = 5.5, 2.4

def rot(a):
    return Rot(0, 0, 90 - a)

def lrect(r0, r1, t0, t1):
    return Pos((r0 + r1)/2, (t0 + t1)/2) * Rectangle(r1 - r0, t1 - t0)

def lbox(r0, r1, t0, t1, z0, z1):
    return Pos((r0 + r1)/2, (t0 + t1)/2, z0) * extrude(Rectangle(r1 - r0, t1 - t0), z1 - z0)

def polar(a, r):
    return Pos(r*math.sin(math.radians(a)), r*math.cos(math.radians(a)))

def holes(points, d):
    sk = None
    for p in points:
        c = p * Circle(d/2)
        sk = c if sk is None else sk + c
    return sk

def arc_sector(r0, r1, a0, a1, n=64):
    po = [(r1*math.sin(math.radians(a)), r1*math.cos(math.radians(a))) for a in [a0 + (a1 - a0)*i/n for i in range(n + 1)]]
    pi = [(r0*math.sin(math.radians(a)), r0*math.cos(math.radians(a))) for a in [a1 - (a1 - a0)*i/n for i in range(n + 1)]]
    return make_face(Polyline(*(po + pi), close=True))

annulus = Circle(OUTER_D/2) - Circle(INNER_D/2)
front_pts = [polar(a, FRONT_R) for a in BRIDGES]
rear_pts = [polar(a, REAR_R) for a in BRIDGES] + [polar(a, REAR_RING_R) for a in REAR_RING_ANGLES]

# --- frame ---
frame_sk = (Circle(OUTER_D/2) - Circle(RING_OUT_IN)) + (Circle(RING_IN_OUT) - Circle(INNER_D/2))
for a in BRIDGES:
    frame_sk += rot(a) * lrect(INNER_D/2 + 1, RING_OUT_IN + 1, -BRIDGE_W/2, BRIDGE_W/2)
frame_sk -= rot(USB_ANGLE) * lrect(0, RING_IN_OUT + 1, -USB_NOTCH_W/2, USB_NOTCH_W/2)   # square mouth, clear plug path
frame_sk -= holes(front_pts + rear_pts, INSERT_HOLE_D)
frame1_sk = frame_sk - (rot(0) * lrect(WIRE_R - WIRE_W/2, WIRE_R + WIRE_W/2, -11, 11)) \
                    - (rot(240) * lrect(WIRE_R - WIRE_W/2, WIRE_R + WIRE_W/2, -11, 11))
frame2_sk = frame_sk
frame_sks = [frame1_sk] + [frame2_sk] * (FRAME_N - 1)     # wire notches in the bottom frame layer only

# --- LED layers ---
def c_bridge(a):
    return rot(a) * lrect(C_CH_IN - 1, C_CH_OUT + 1, -BRIDGE_W/2, BRIDGE_W/2)
c_channel = Circle(C_CH_OUT) - Circle(C_CH_IN)
led_base = Circle(WOOD_OUT_R) - Circle(INNER_D/2)
led1_sk = led_base - c_channel
for a in BRIDGES:
    led1_sk += c_bridge(a) & c_channel
led2_sk = led_base - (c_channel - c_bridge(0))
led1_sk -= holes(front_pts, SCREW_CLR_D)
led2_sk -= holes(front_pts, SCREW_CLR_D)

# --- white ring, face, C ---
white_sk = Circle(OUTER_D/2) - Circle(WHITE_IN_R)
g = math.radians(C_GAP_DEG/2)
gap = make_face(Polyline((0, 0), (100*math.sin(g), 100*math.cos(g)), (-100*math.sin(g), 100*math.cos(g)), close=True))
c_sk = (Circle(C_OUT_R) - Circle(C_IN_R)) - gap
face_sk = Circle(FACE_OUT_R) - Circle(INNER_D/2) - c_sk - holes(front_pts, SCREW_CLR_D)

# --- buttons on the back ---
btn_loc = rot(BTN_ANGLE) * Pos(BTN_R, 0)
def board_pt(l, w):           # board coords: l along the board (tangential), w across it (radial, + outward)
    return btn_loc * Pos(w, l)
btn_pts = [(BTN_OFF_L + (i - 1.5)*BTN_PITCH, BTN_OFF_W) for i in range(4)]
mount_pts = [(sx*MOUNT_DX, sy*MOUNT_DY) for sx in (-1, 1) for sy in (-1, 1)]
sq = SW + 2*SW_CLR
btn_cut = None
for l, w in btn_pts:
    s = board_pt(l, w) * fillet(Rectangle(sq, sq).vertices(), 0.5)
    btn_cut = s if btn_cut is None else btn_cut + s

# --- battery ---
hold_loc = rot(HOLDER_ANGLE) * Pos(HOLDER_IN + HOLDER_W/2, 0)
win_w, win_l = HOLDER_W + 2*HOLDER_CLR, HOLDER_L + 2*HOLDER_CLR
window_sk = hold_loc * fillet(Rectangle(win_w, win_l).vertices(), 0.5)
holder_bot = -ACRYLIC_T - BOX_RINGS*ACRYLIC_T     # the holder stands on the floor
holder_top = holder_bot + HOLDER_H
box_floor_bot = holder_bot - ACRYLIC_T
box_screw_pts = [hold_loc * Pos(a, b) for a, b in BOX_SCREWS]

# --- back ---
pod_loc = rot(USB_ANGLE) * Pos(POD_R0, 0)
back_sk = annulus - window_sk - btn_cut \
    - holes([board_pt(l, w) for l, w in mount_pts], MOUNT_D) \
    - holes(rear_pts, SCREW_CLR_D) - holes(box_screw_pts, BOX_SCREW_HOLE) \
    - holes([pod_loc * Pos(x, y) for x, y in POD_SCREWS], POD_SCREW_HOLE) \
    - rot(USB_ANGLE) * lrect(0, INNER_D/2, -USB_NOTCH_W/2, USB_NOTCH_W/2)   # flat at the hand hole, matching the frame notch

# --- solids ---
back = Pos(0, 0, -ACRYLIC_T) * extrude(back_sk, ACRYLIC_T)
frames = [Pos(0, 0, i*PLY_T) * extrude(s, PLY_T) for i, s in enumerate(frame_sks)]
led1 = Pos(0, 0, FRAME_H) * extrude(led1_sk, PLY_T)
led2 = Pos(0, 0, FRAME_H + PLY_T) * extrude(led2_sk, PLY_T)
white_ring = Pos(0, 0, FRAME_H) * extrude(white_sk, WHITE_T)
z_face = FRAME_H + 2*PLY_T
face = Pos(0, 0, z_face) * extrude(face_sk, ACRYLIC_T)
white_c = Pos(0, 0, z_face) * extrude(c_sk, ACRYLIC_T)

# battery box: BOX_RINGS rings, then the floor
box_outline = fillet(Rectangle(2*BOX_HALF_W, 2*BOX_HALF_L).vertices(), 3.0)
box_holes = holes([Pos(a, b) for a, b in BOX_SCREWS], BOX_SCREW_HOLE)
ring_sk = box_outline - fillet(Rectangle(win_w, win_l).vertices(), 0.5) - box_holes
floor_sk = box_outline - box_holes - Circle(BOX_SCREW_D/2)
box_parts = [hold_loc * Pos(0, 0, -ACRYLIC_T - (i + 1)*ACRYLIC_T) * extrude(ring_sk, ACRYLIC_T) for i in range(BOX_RINGS)] + \
            [hold_loc * Pos(0, 0, box_floor_bot) * extrude(floor_sk, ACRYLIC_T)]
# black M3 button heads from outside, nuts on the inside face of the back
BOX_SCREW_L = 16.0
box_hw = []
for pt in box_screw_pts:
    box_hw += [pt * Pos(0, 0, box_floor_bot - 1.65) * Cylinder(2.85, 1.65, align=(Align.CENTER, Align.CENTER, Align.MIN)),
               pt * Pos(0, 0, box_floor_bot) * Cylinder(1.5, BOX_SCREW_L, align=(Align.CENTER, Align.CENTER, Align.MIN)),
               pt * extrude(RegularPolygon(NUT_AF/math.sqrt(3), 6) - Circle(1.5), NUT_H)]
battery_box = Compound(children=[b.moved(Location()) for b in box_parts])   # copies: a Compound takes ownership of its children

# --- reference parts ---
# 18650 holder, from the photos: open tray, tall end walls, low side walls with two raised clip
# sections, spring at one end. Local frame: x across (21), y along (80), z up from the holder's base.
def holder_tray():
    base_t, end_t, side_t = 1.5, 2.0, 1.2
    tray = Pos(0, 0, 0) * extrude(Rectangle(HOLDER_W, HOLDER_L), base_t)
    end = fillet(Rectangle(HOLDER_W, HOLDER_H).vertices().group_by(Axis.Y)[-1], 3.0)
    for sy in (-1, 1):
        tray += Pos(0, sy*(HOLDER_L/2 - end_t/2), 0) * Rot(90, 0, 0) * Pos(0, HOLDER_H/2) * extrude(end, end_t/2, both=True)
    low_h, clip_h, clip = 8.0, 14.0, ((-31.0, -9.0), (9.0, 31.0))
    for sx in (-1, 1):
        prof = Polyline((-HOLDER_L/2 + end_t, 0), (HOLDER_L/2 - end_t, 0), (HOLDER_L/2 - end_t, low_h),
                        (clip[1][1] + 2, low_h), (clip[1][1], clip_h), (clip[1][0], clip_h), (clip[1][0] - 2, low_h),
                        (clip[0][1] + 2, low_h), (clip[0][1], clip_h), (clip[0][0], clip_h), (clip[0][0] - 2, low_h),
                        (-HOLDER_L/2 + end_t, low_h), close=True)
        wall = Pos(sx*(HOLDER_W/2 - side_t/2), 0, 0) * extrude(Plane.YZ * make_face(prof), side_t/2, both=True)
        tray += wall
    # the single mounting hole, countersunk from inside
    tray -= Cylinder(1.7, base_t, align=(Align.CENTER, Align.CENTER, Align.MIN))
    tray -= Pos(0, 0, base_t - 1.65) * Cone(1.5, 2.9, 1.65, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return tray

CELL_D, CELL_L = 18.3, 65.2        # Samsung INR18650-30Q
def holder_cell():
    c = Cylinder(CELL_D/2, CELL_L, rotation=(90, 0, 0))
    c += Pos(0, CELL_L/2, 0) * Cylinder(2.5, 1.0, rotation=(90, 0, 0), align=(Align.CENTER, Align.CENTER, Align.MAX))   # + button
    y0 = -HOLDER_L/2 + 2.0                      # flat contact end
    return Pos(0, y0 + CELL_L/2, 1.5 + CELL_D/2 + 0.3) * c

def holder_spring():
    y1 = -HOLDER_L/2 + 2.0 + CELL_L + 1.0
    coils = None
    for i in range(6):
        ring = Pos(0, y1 + i*(HOLDER_L/2 - 2.0 - y1)/5.5, 1.5 + CELL_D/2 + 0.3) * Rot(90, 0, 0) * \
            (Cylinder(3.65, 0.9) - Cylinder(2.75, 0.9))       # flat rings: light enough for the 3D board
        coils = ring if coils is None else coils + ring
    return coils

holder = hold_loc * Pos(0, 0, holder_bot) * (holder_tray() + holder_spring())
cell = hold_loc * Pos(0, 0, holder_bot) * holder_cell()
board = btn_loc * Pos(0, 0, SW_STANDOFF) * extrude(Rectangle(BOARD_W, BOARD_L), BOARD_T)
switches = [board_pt(l, w) * Pos(0, 0, SW_STANDOFF - SW_H) * extrude(Rectangle(SW, SW), SW_H) for l, w in btn_pts]
caps = [board_pt(l, w) * Pos(0, 0, SW_STANDOFF - SW_H - 1.5) * extrude(Circle(1.75), 1.5) for l, w in btn_pts]
# --- electronics pod (built in its local frame, placed with pod_loc) ---
def pbox(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1)/2, (y0 + y1)/2, z0) * extrude(Rectangle(x1 - x0, y1 - y0), z1 - z0)

def usbc(y0, y1, t):
    yc = (y0 + y1)/2
    shell = pbox(BOARD_X0 - USBC_OUT, BOARD_X0 - USBC_OUT + USBC_L, yc - USBC_W/2, yc + USBC_W/2, t, t + USBC_H)
    return fillet(shell.edges().filter_by(Axis.X), 1.2)

def board_parts(name):
    """(pcb, metal, parts, extra) solids for one board, from the photos."""
    y0, y1, L, t = PODS[name]
    x0, x1, yc = BOARD_X0, BOARD_X0 + L, (y0 + y1)/2
    pcb = pbox(x0, x1, y0, y1, 0, t)
    metal, parts, extra = [], [], []
    if name == "tp4056":
        metal.append(usbc(y0, y1, t))
        parts += [pbox(x0 + 12, x0 + 17, yc - 3, yc + 2, t, t + 1.5),          # TP4056 SOP-8
                  pbox(x0 + 19, x0 + 24, y0 + 2, y0 + 6, t, t + 1.5)]           # DW01 protection
        for i in range(4):                                                     # B+ B- OUT+ OUT- pads at the far end
            metal.append(pbox(x1 - 3, x1 - 0.8, y0 + 1.5 + i*4.0, y0 + 3.7 + i*4.0, t, t + 0.1))
    elif name == "mt3608":
        extra.append(pbox(x0 + 3, x0 + 12.5, y0 + 3.5, y0 + 13.5, t, t + 7.0))        # blue trimpot
        parts += [pbox(x0 + 17, x0 + 23, yc - 3, yc + 3, t, t + 4.5),              # inductor
                  pbox(x0 + 25, x0 + 29, y0 + 2, y0 + 5, t, t + 2.0)]              # diode
        for xa in (x0 + 0.8, x1 - 4.8):                                            # VIN / VOUT pads at both ends
            for ya in (y0 + 1, y1 - 5):
                metal.append(pbox(xa, xa + 4, ya, ya + 4, t, t + 0.1))
    else:
        metal.append(usbc(y0, y1, t))
        parts += [pbox(x0 + 11, x0 + 16, yc - 2.5, yc + 2.5, t, t + 0.9),          # ESP32-C3
                  pbox(x0 + 8, x0 + 11, y0 + 3, y0 + 7, t, t + 1.6),               # BOOT
                  pbox(x0 + 8, x0 + 11, y1 - 7, y1 - 3, t, t + 1.6)]               # RST
        for i in range(8):                                                     # castellated pins down both long edges
            xc = x0 + 4 + i*2.54
            pcb -= Pos(xc, y0) * Cylinder(0.5, 2*t) + Pos(xc, y1) * Cylinder(0.5, 2*t)
    return pcb, metal, parts, extra

pod_pcbs, pod_metal, pod_ics, pod_extra = {}, [], [], []
_mt = PODS["mt3608"]
mt_xf = Pos(MT_X0 + (_mt[1] - _mt[0])/2, 0) * Rot(0, 0, 90) * Pos(-(BOARD_X0 + _mt[2]/2), 0)   # MT3608: turn sideways, set behind
for nm in PODS:
    pcb, metal, parts, extra = board_parts(nm)
    xf = pod_loc * (mt_xf if nm == "mt3608" else Location())
    pod_pcbs[nm] = xf * pcb
    pod_metal += [xf * m for m in metal]; pod_ics += [xf * m for m in parts]; pod_extra += [xf * m for m in extra]

# back part of the carrier outline: y +-BACK_HALF_W, back corners rounded to stay off the frame
cover_sk = Pos(POD_X1/2, 0) * Rectangle(POD_X1, 2*BACK_HALF_W)
cover_sk = fillet(cover_sk.vertices().filter_by(lambda v: v.X > POD_X1/2), POD_BACK_R)
# plate: the cover outline, widened at the front for the screw tabs
plate_sk = cover_sk + Pos(18.0, 0) * fillet(Rectangle(36.0, 2*POD_HALF_W).vertices(), 2.0)
pod_holes = holes([Pos(x, y) for x, y in POD_SCREWS], POD_SCREW_HOLE)
locator_sk = plate_sk - pod_holes
holddown_sk = plate_sk - pod_holes
for nm, (y0, y1, L, t) in PODS.items():
    if nm == "mt3608":
        # behind the others: a closed pocket and a window with a rim all round
        mx1 = MT_X0 + (y1 - y0)
        locator_sk -= Pos((MT_X0 + mx1)/2, 0) * Rectangle(mx1 - MT_X0 + 2*POD_CLR, L + 2*POD_CLR)
        holddown_sk -= Pos((MT_X0 + mx1)/2, 0) * Rectangle(mx1 - MT_X0 - 2*POD_RIM, L - 2*POD_RIM)
        continue
    # locator: a pocket per board, open at the front
    locator_sk -= Pos((BOARD_X0 + L + POD_CLR - 1)/2, (y0 + y1)/2) * Rectangle(BOARD_X0 + L + POD_CLR + 1, y1 - y0 + 2*POD_CLR)
    # hold-down: a window per board, leaving a rim over its back end and sides; open at the front for USB-C
    wx1 = BOARD_X0 + L - POD_RIM
    holddown_sk -= Pos((wx1 - 1)/2, (y0 + y1)/2) * Rectangle(wx1 + 1, y1 - y0 - 2*POD_RIM)
# face plate: black 3 mm, standing at the hand hole (pod x -3..0), as wide as the frame notch and just under the
# frame height. Cemented along its bottom edge to the back. Openings only for the two USB-C ports, open at the bottom
# so no thin strip is left under them.
FP_HALF_W, FP_H = USB_NOTCH_W/2 - FP_CLR, FRAME_H - 0.5
fp_sk = Pos(0, FP_H/2) * Rectangle(2*FP_HALF_W, FP_H)
for nm in ("tp4056", "esp32c3"):
    y0, y1, L, t = PODS[nm]; yc = (y0 + y1)/2
    sw, sh = USBC_W + 2*FP_SLOT_CLR, t + USBC_H + FP_SLOT_CLR
    fp_sk -= Pos(yc, sh/2 - 0.5) * Rectangle(sw, sh + 1)
face_plate = pod_loc * Pos(-FP_T, 0, 0) * extrude(Plane.YZ * fp_sk, FP_T)
pod_locator = pod_loc * extrude(locator_sk, POD_LOC_T)
pod_holddown = pod_loc * Pos(0, 0, POD_LOC_T) * extrude(holddown_sk, POD_PLATE_T)
pod_hw = []
for x, y in POD_SCREWS:
    pt = pod_loc * Pos(x, y)
    pod_hw += [pt * Pos(0, 0, -ACRYLIC_T - 1.3) * Cylinder(1.9, 1.3, align=(Align.CENTER, Align.CENTER, Align.MIN)),
               pt * Pos(0, 0, -ACRYLIC_T) * Cylinder(1.0, POD_SCREW_L, align=(Align.CENTER, Align.CENTER, Align.MIN)),
               pt * Pos(0, 0, POD_LOC_T + POD_PLATE_T) * extrude(RegularPolygon(M2_NUT_AF/math.sqrt(3), 6) - Circle(1.0), M2_NUT_H)]
usb_boards = list(pod_pcbs.values())     # board outlines, for clearance checks

# --- LED path: GPIO -> C strip input (350 deg) -> C runs to 10 deg -> jumper -> outer strip start (12 deg).
# One 3-wire bundle (5 V, ground, data) drops from the C input to an in-line connector on the back, so the back
# (with the pod) unplugs from the strips. Wires drawn as 2.5 mm bundles.
def P(a, r, z):
    return Vector(r*math.sin(math.radians(a)), r*math.cos(math.radians(a)), z)
def tube(pts, d=2.5):
    segs = []
    for a_, b_ in zip(pts, pts[1:]):
        v = b_ - a_
        segs.append(Pos(a_) * Solid.make_cylinder(d/2, v.length, Plane(origin=(0, 0, 0), z_dir=v)))
    segs += [Pos(q) * Sphere(d/2) for q in pts]
    return segs
CONN_A, CONN_R, CONN_L, CONN_W, CONN_H = 333.0, 99.0, 25.0, 7.5, 6.0     # in-line 3-pin connector pair (JST-SM size)
conn = rot(CONN_A) * lbox(CONN_R - CONN_W/2, CONN_R + CONN_W/2, -CONN_L/2, CONN_L/2, 0, CONN_H)
conn_end_strip = P(CONN_A + math.degrees(CONN_L/2/CONN_R), CONN_R, CONN_H/2)
conn_end_pod = P(CONN_A - math.degrees(CONN_L/2/CONN_R), CONN_R, CONN_H/2)
c_mid = (C_CH_OUT - STRIP_T/2)
z_pod_top = POD_LOC_T + POD_PLATE_T
pod_exit = (pod_loc * Pos(40.0, -BACK_HALF_W - 1.5)).position + Vector(0, 0, z_pod_top + 1.5)
pod_inside = (pod_loc * Pos(40.0, -BACK_HALF_W + 4)).position + Vector(0, 0, z_pod_top + 1.5)
wire_strip_side = tube([P(350, c_mid, FRAME_H + PLY_T + STRIP_W/2), P(350, c_mid, CONN_H/2), conn_end_strip])
wire_pod_side = tube([conn_end_pod, pod_exit, pod_inside])
jumper = tube([P(10, c_mid, FRAME_H + PLY_T + STRIP_W/2), P(10, c_mid, 12.0), P(12, 108.5, 12.0), P(12, 108.5, FRAME_H + (WHITE_T - STRIP_W)/2)])
led_strip = Pos(0, 0, FRAME_H + (WHITE_T - STRIP_W)/2) * extrude(Circle(WHITE_IN_R) - Circle(WOOD_OUT_R), STRIP_W)
c_strip = Pos(0, 0, FRAME_H + PLY_T) * extrude(arc_sector(C_CH_OUT - STRIP_T, C_CH_OUT, C_GAP_DEG/2, 360 - C_GAP_DEG/2), STRIP_W)

INSERT_CORE_D = 8.0                  # root of the coarse outer thread
INSERT_PITCH, INSERT_CREST = 2.0, 0.9
INSERT_FLANGE_D, INSERT_FLANGE_H = 10.8, 1.2   # slightly flared end, the hex end (from the product photo)
INSERT_HEX_AF, INSERT_HEX_DEPTH = 6.0, 3.0     # hex drive for the spanner

def insert_solid():
    # built hex end up at z = INSERT_L, threads below
    body = Cylinder(INSERT_CORE_D/2, INSERT_L, align=(Align.CENTER, Align.CENTER, Align.MIN))
    z = 1.0
    while z + INSERT_CREST < INSERT_L - INSERT_FLANGE_H:
        body += Pos(0, 0, z) * Cylinder(INSERT_D/2, INSERT_CREST, align=(Align.CENTER, Align.CENTER, Align.MIN))
        z += INSERT_PITCH
    body += Pos(0, 0, INSERT_L - INSERT_FLANGE_H) * Cone(INSERT_D/2, INSERT_FLANGE_D/2, INSERT_FLANGE_H,
                                                          align=(Align.CENTER, Align.CENTER, Align.MIN))
    body -= Cylinder(2.0, INSERT_L, align=(Align.CENTER, Align.CENTER, Align.MIN))     # M4 bore
    body -= Pos(0, 0, INSERT_L - INSERT_HEX_DEPTH) * extrude(RegularPolygon(INSERT_HEX_AF/math.sqrt(3), 6), INSERT_HEX_DEPTH)
    return body

_insert = insert_solid()
def insert_at(p, from_top):
    # front inserts: hex end up at the frame top; rear inserts: hex end down at the frame bottom
    if from_top:
        return p * Pos(0, 0, FRAME_H - INSERT_L) * _insert
    return p * Pos(0, 0, INSERT_L) * Rot(180, 0, 0) * _insert
inserts = Compound(children=[insert_at(p, True) for p in front_pts] + [insert_at(p, False) for p in rear_pts])

# black M4 button-head screws (ISO 7380: head 7.6 across, 2.2 tall)
HEAD_D, HEAD_H = 7.6, 2.2
FRONT_SCREW_L = 20.0                         # M4 x 20: face + LED layers, 7 mm into the insert
REAR_SCREW_L = 12.0                          # M4 x 12: back, 9 mm into the insert
def screw(p, z_head, length, down):
    head = p * Pos(0, 0, z_head if down else z_head - HEAD_H) * Cylinder(HEAD_D/2, HEAD_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
    z0 = z_head - length if down else z_head
    shank = p * Pos(0, 0, z0) * Cylinder(2.0, length, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return [head, shank]
z_top = FRAME_H + 2*PLY_T + ACRYLIC_T
front_screws = Compound(children=[s for p in front_pts for s in screw(p, z_top, FRONT_SCREW_L, True)])
rear_screws = Compound(children=[s for p in rear_pts for s in screw(p, -ACRYLIC_T, REAR_SCREW_L, False)])

assembly = Compound(children=[back, *frames, led1, led2, white_ring, face, white_c, *box_parts])

# names match the files in cad/v2/
for i, (sk, sol) in enumerate(zip(frame_sks, frames), 1):
    show(sk, f"frame{i}_outline"); show(sol, f"frame{i}")
for name, shape in [("led1_outline", led1_sk), ("led1", led1), ("led2_outline", led2_sk), ("led2", led2),
                    ("back_outline", back_sk), ("back", back),
                    ("white_ring_outline", white_sk), ("white_ring", white_ring),
                    ("face_outline", face_sk), ("face", face), ("c_outline", c_sk), ("white_c", white_c),
                    ("box_ring_outline", ring_sk), ("box_hardware_ref", Compound(children=box_hw)),
                    ("box_floor_outline", floor_sk), ("battery_box", battery_box),
                    ("holder_ref", holder), ("cell_ref", cell), ("buttons_ref", Compound(children=[board, *switches, *caps])),
                    ("electronics_ref", Compound(children=[b.moved(Location()) for b in usb_boards])), ("inserts_ref", inserts),
                    ("pod_locator_outline", locator_sk), ("pod_holddown_outline", holddown_sk),
                    ("pod_locator", pod_locator), ("pod_holddown", pod_holddown),
                    ("pod_pcb_blue", Compound(children=[pod_pcbs["tp4056"].moved(Location()), pod_pcbs["mt3608"].moved(Location())])),
                    ("pod_pcb_black", pod_pcbs["esp32c3"].moved(Location())),
                    ("pod_metal", Compound(children=[m.moved(Location()) for m in pod_metal])),
                    ("pod_ics", Compound(children=[m.moved(Location()) for m in pod_ics])),
                    ("pod_trimpot", Compound(children=[m.moved(Location()) for m in pod_extra])),
                    ("pod_hardware", Compound(children=[m.moved(Location()) for m in pod_hw])),
                    ("face_plate_outline", fp_sk), ("face_plate", face_plate),
                    ("led_connector", conn), ("led_wire_strip", Compound(children=wire_strip_side)),
                    ("led_wire_pod", Compound(children=wire_pod_side)), ("led_jumper", Compound(children=jumper)),
                    ("front_screws_ref", front_screws), ("rear_screws_ref", rear_screws),
                    ("led_strip_ref", led_strip), ("c_strip_ref", c_strip)]:
    show(shape, name)
# --- battery box detail: the same parts in the holder's own frame (x across, y along, z as in the disc),
# with a piece of the back and the frame/LED layers above for context. Exported to cad/v2/battery/.
to_batt = hold_loc.inverse() if hasattr(hold_loc, "inverse") else Location(hold_loc).inverse()
crop = Pos(0, 0, -20) * Box(70, 130, 60, align=(Align.CENTER, Align.CENTER, Align.MIN))
def batt(shape):
    return to_batt * shape.moved(Location())
def batt_crop(shape):
    return (batt(shape)) & crop
HOLDER_SCREW_L = 8.0                  # M3 x 8 flat head down through the holder base and the floor, nut outside
hs_z = holder_bot + 1.5               # top of the holder's base
batt_parts = {
    "back_piece": batt_crop(back),
    "frame_piece": batt_crop(frames[0]) + batt_crop(frames[1]) + batt_crop(frames[2]),
    "led_piece": batt_crop(led1) + batt_crop(led2),
    "ring1": batt(box_parts[0]), "ring2": batt(box_parts[1]), "floor": batt(box_parts[2]),
    "holder": batt(holder), "cell": batt(cell),
    "box_screws": Compound(children=[batt(h) for h in box_hw]),
    "holder_screw": Compound(children=[
        Pos(0, 0, hs_z - 1.65) * Cone(1.5, 2.8, 1.65, align=(Align.CENTER, Align.CENTER, Align.MIN)),
        Pos(0, 0, hs_z - HOLDER_SCREW_L) * Cylinder(1.5, HOLDER_SCREW_L, align=(Align.CENTER, Align.CENTER, Align.MIN)),
        Pos(0, 0, box_floor_bot - NUT_H) * extrude(RegularPolygon(NUT_AF/math.sqrt(3), 6) - Circle(1.5), NUT_H)]),
}
for k, v in batt_parts.items():
    show(v, f"batt_{k}")

# --- electronics pod detail: the pod in its own frame (x from R61 outward, y sideways, z as in the disc),
# with a piece of the back and the frame/LED layers for context, plus a USB-C plug. Exported to cad/v2/pod/.
to_pod = pod_loc.inverse()
pod_crop = Pos(15, 0, -20) * Box(80, 100, 60, align=(Align.CENTER, Align.CENTER, Align.MIN))
def podl(shape):
    return to_pod * shape.moved(Location())
def plug_ref(name):
    y0, y1, L, t = PODS[name]; yc, zc_ = (y0 + y1)/2, t + USBC_H/2
    body = Pos(-FP_T - 16, yc, zc_ - 3.25) * Box(16, PLUG_W, 6.5, align=(Align.MIN, Align.CENTER, Align.MIN))     # grip stops at the face plate
    tongue = Pos(-FP_T, yc, zc_ - 1.25) * Box(FP_T - USBC_OUT, 8.3, 2.5, align=(Align.MIN, Align.CENTER, Align.MIN))  # metal shell through the opening
    cable = Pos(-FP_T - 28, yc, zc_) * Rot(0, 90, 0) * Cylinder(2.0, 12, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return Compound(children=[body, tongue, cable])   # a reference USB-C plug, seated
pod_parts = {
    "back_piece": podl(back) & pod_crop,
    "frame_piece": (podl(frames[0]) & pod_crop) + (podl(frames[1]) & pod_crop) + (podl(frames[2]) & pod_crop),
    "led_piece": (podl(led1) & pod_crop) + (podl(led2) & pod_crop),
    "locator": podl(pod_locator), "holddown": podl(pod_holddown),
    "pcb_blue": Compound(children=[podl(pod_pcbs["tp4056"]), podl(pod_pcbs["mt3608"])]),
    "pcb_black": podl(pod_pcbs["esp32c3"]),
    "metal": Compound(children=[podl(m) for m in pod_metal]),
    "ics": Compound(children=[podl(m) for m in pod_ics]),
    "trimpot": Compound(children=[podl(m) for m in pod_extra]),
    "hardware": Compound(children=[podl(m) for m in pod_hw]),
    "plugs": Compound(children=[*plug_ref("tp4056").children, *plug_ref("esp32c3").children]),
    "face_plate": podl(face_plate),
}
for k, v in pod_parts.items():
    show(v, f"podlocal_{k}")       # not "pod_": those names are the pod in the disc

# test strip: drawn pilot sizes for the M4 x 12 inserts; pick the snug one and set INSERT_HOLE_D
TEST_DS = [7.4, 7.6, 7.8, 8.0, 8.2, 8.4]
insert_test = fillet(Rectangle(14*len(TEST_DS) + 6, 22).vertices(), 1.0)
for i, d in enumerate(TEST_DS):
    insert_test -= Pos((i - (len(TEST_DS) - 1)/2) * 14, -2) * Circle(d/2)
show(insert_test, "insert_test_outline")
show(Compound(children=[back, *frames, led1, led2, white_ring, face, white_c, *[b.moved(Location()) for b in box_parts]]), "assembly")
result = assembly

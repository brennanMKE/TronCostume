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
WIRE_W, WIRE_R = 6.0, 92.5           # wire notch across bridges 0 and 240, top frame layer

# buttons: protoboard screwed to the inside of the back, switches facing out
BTN_ANGLE, BTN_R = 60, 90.0          # board center
BOARD_L, BOARD_W, BOARD_T = 80.0, 20.0, 1.6
SW, SW_H, SW_CLR = 6.0, 3.5, 0.2     # 6x6 switch body, its height, hole clearance per side
SW_STANDOFF = 0.0                    # gap between switch body and board - measure
BTN_PITCH = 10.0                     # 36 across four 6 mm switches with 4 mm gaps
BTN_OFF_L, BTN_OFF_W = -3.8, -4.0    # button row center from board center (from the photo - measure)
MOUNT_DX, MOUNT_DY, MOUNT_D = 37.0, 7.5, 2.4   # M2 corner holes (estimated - measure)

# USB: charger + ESP32-C3 in an acrylic pod (carrier + cemented black cover), ports facing the
# hand hole through a notch in the inner ring. Rough envelope only - detailed in its own model.
USB_ANGLE, USB_NOTCH_W = 300, 52.0
POD_R0 = 61.0                        # pod front face, 1 mm behind the hand hole
POD_WALL, POD_CARRIER_T, POD_TOP_T = 3.0, 3.0, 3.0
POD_INNER_H = 7.0                    # boards 4.5 tall + 2.5, so a plug overmold clears the top
POD_LEN, POD_W = 36.0, 48.0          # radial x tangential, outside
PORT_R = POD_R0 + POD_WALL           # board USB-C ends at the front wall's inside face
CHARGER_T = (-20.0, -3.0)            # tangential span, TP4056 17 x 28
ESP_T = (2.0, 20.0)                  # ESP32-C3 Super Mini 18 x 22.5
PLUG_W = 13.0                        # slot width for a USB-C plug overmold (about 12.4 wide)
MT_R, MT_T = (78.0, 95.8), (27.0, 59.8)   # MT3608 32.8 x 17.8, beside the pod on the back

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
frame1_sk = frame_sk
frame2_sk = frame_sk - (rot(0) * lrect(WIRE_R - WIRE_W/2, WIRE_R + WIRE_W/2, -11, 11)) \
                    - (rot(240) * lrect(WIRE_R - WIRE_W/2, WIRE_R + WIRE_W/2, -11, 11))
frame_sks = [frame1_sk] * (FRAME_N - 1) + [frame2_sk]     # wire notches in the top frame layer only

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
back_sk = annulus - window_sk - btn_cut \
    - holes([board_pt(l, w) for l, w in mount_pts], MOUNT_D) \
    - holes(rear_pts, SCREW_CLR_D) - holes(box_screw_pts, BOX_SCREW_HOLE)

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
# all electronics sit on the inside of the back and come away with it
zb = POD_CARRIER_T                   # boards sit on the carrier
usb_boards = [
    rot(USB_ANGLE) * lbox(PORT_R, PORT_R + 28.0, *CHARGER_T, zb, zb + 4.5),
    rot(USB_ANGLE) * lbox(PORT_R, PORT_R + 22.5, *ESP_T, zb, zb + 4.5),
    rot(USB_ANGLE) * lbox(*MT_R, *MT_T, 0, 6.0),                         # MT3608 boost, straight on the back
]

# pod: carrier plate, cemented cover (two side walls, back wall, top, front posts between plug slots)
r1, w2, z_in = POD_R0 + POD_LEN, POD_W/2, POD_CARRIER_T + POD_INNER_H
slots = [((t0 + t1)/2 - PLUG_W/2, (t0 + t1)/2 + PLUG_W/2) for t0, t1 in (CHARGER_T, ESP_T)]
posts, t = [], -w2 + POD_WALL
for s0, s1 in slots:
    posts.append((t, s0)); t = s1
posts.append((t, w2 - POD_WALL))
pod_carrier = rot(USB_ANGLE) * lbox(PORT_R, r1, -w2, w2, 0, POD_CARRIER_T)   # starts behind the front wall
pod_cover = [rot(USB_ANGLE) * lbox(POD_R0, PORT_R, -w2, -w2 + POD_WALL, 0, POD_CARRIER_T),
             rot(USB_ANGLE) * lbox(POD_R0, PORT_R, w2 - POD_WALL, w2, 0, POD_CARRIER_T),
             rot(USB_ANGLE) * lbox(POD_R0, r1, -w2, -w2 + POD_WALL, POD_CARRIER_T, z_in),
             rot(USB_ANGLE) * lbox(POD_R0, r1, w2 - POD_WALL, w2, POD_CARRIER_T, z_in),
             rot(USB_ANGLE) * lbox(r1 - POD_WALL, r1, -w2 + POD_WALL, w2 - POD_WALL, POD_CARRIER_T, z_in),
             rot(USB_ANGLE) * lbox(POD_R0, r1, -w2, w2, z_in, z_in + POD_TOP_T)] + \
            [rot(USB_ANGLE) * lbox(POD_R0, PORT_R, a, b, 0, z_in) for a, b in posts if b - a > 0.5]
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
                    ("electronics_ref", Compound(children=usb_boards)), ("inserts_ref", inserts),
                    ("pod_carrier", pod_carrier), ("pod_cover", Compound(children=[c.moved(Location()) for c in pod_cover])),
                    ("front_screws_ref", front_screws), ("rear_screws_ref", rear_screws),
                    ("led_strip_ref", led_strip), ("c_strip_ref", c_strip)]:
    show(shape, name)
# test strip: drawn pilot sizes for the M4 x 12 inserts; pick the snug one and set INSERT_HOLE_D
TEST_DS = [7.4, 7.6, 7.8, 8.0, 8.2, 8.4]
insert_test = fillet(Rectangle(14*len(TEST_DS) + 6, 22).vertices(), 1.0)
for i, d in enumerate(TEST_DS):
    insert_test -= Pos((i - (len(TEST_DS) - 1)/2) * 14, -2) * Circle(d/2)
show(insert_test, "insert_test_outline")
show(Compound(children=[back, *frames, led1, led2, white_ring, face, white_c, *[b.moved(Location()) for b in box_parts]]), "assembly")
result = assembly

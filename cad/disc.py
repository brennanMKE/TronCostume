"""Tron identity disc: parametric layer stack (build123d). All dimensions mm.

Angles are clockwise from 12 o'clock seen from the front. In a bay's local
frame, x is radial (out from the center) and y is tangential.

Run in the build123d-mcp server with execute_file(); every part is registered
with show() under the names the exports use. Cut-file SVGs need their stroke
changed to red 0.1 mm after export (see docs/cad-status.md).
"""
import math
from build123d import *

# --- overall ---
OUTER_D, INNER_D = 260.0, 120.0
ACRYLIC_T = 3.0                    # black back, black face, white C, covers
PLY_T = 5.0                        # maple, "about 5" - measure
WHITE_T = 10.0                     # white outer ring

# --- bottom bays (layers 1-3) ---
WALL_IN_R, WALL_OUT_R = 66.0, 120.0
RIB_W, RIB_ANGLES = 20.0, (0, 120, 240)
WIRE_W, WIRE_R = 8.0, 93.0

# --- LED layers (4-5) ---
C_CH_IN, C_CH_OUT = 80.0, 96.0     # C light channel; C strip on the R96 wall, layer 5
WHITE_IN_R = 110.0                 # white ring R110-R130
STRIP_T, STRIP_W = 3.0, 5.0
WOOD_OUT_R = WHITE_IN_R - STRIP_T  # wood stops at R107; outer strip R107-R110
C_GAP_DEG, BRIDGE_W = 20.0, 20.0

# --- face ---
FACE_OUT_R = 114.0                 # overlaps the white ring 4 mm as a cement land
C_IN_R, C_OUT_R = 82.0, 88.0

# --- battery holder ---
HOLDER_L, HOLDER_W, HOLDER_H = 80.0, 21.0, 22.0
HOLDER_CLR, HOLDER_ANGLE, HOLDER_IN = 0.5, 180, 70.5
SOCK_CLR, SOCK_WALL = 0.25, 4.0

# --- bay covers ---
BAYS = {"buttons": 60, "usb": 300}
COVER_L, COVER_IN = 90.0, 61.0
COVER_Z0, COVER_Z1 = 0.25, 24.75
CLR = 0.25
SCREW_D, BTN_D = 4.5, 4.0
INSERT_D, INSERT_L = 8.0, 10.0     # assumed - measure
BOARD_L, BOARD_H, BOARD_T = 80.0, 20.0, 1.6
SLOT_W, SW_BODY = 1.5, 3.5
BTN_PITCH = 15.24
TAB_OUT = 58.0
TAB_Z1 = 3*PLY_T - 0.25
BLK_T0, BLK_T1 = 44.5, 56.5
SCREW_X, SCREW_Z = 50.5, 7.5
FRAME_T0, FRAME_T1 = BOARD_L/2 + 1.5, 62.0

# --- lid/base split: lid = face, white C, white ring, layers 4-5; base = back, layers 1-3 ---
LID_SCREW_R = (72.0, 103.0)        # at the rib/bridge angles: clear of the C, the channel and the bay cuts
LID_SCREW_L = 25.0                 # M4 x 25 button head (ISO 7380); countersunk would leave 0.7 of the face
HEAD_D, HEAD_H, SHANK_D = 7.6, 2.2, 4.0
INSERT_HOLE_D = 6.5                # pilot for a screw-in wood insert, INSERT_D x INSERT_L - measure
SLOT4_W = 2.0                      # lid side of the board slot: loose, so the lid drops back over the board
CONN_A, CONN_R = 340, 108.0        # 3-pin LED connector, in the bay below the strips; clears the USB bay frame
CONN_L, CONN_W, CONN_H = 30.0, 8.0, 10.0

cover_back = COVER_IN + ACRYLIC_T
BOARD_Y = cover_back + SW_BODY
BTN_Z = BOARD_H/2
BLK_Y1 = cover_back + 12.25
COVER_H = COVER_Z1 - COVER_Z0
zc = (COVER_Z0 + COVER_Z1)/2


def rot(a):
    return Rot(0, 0, 90 - a)


def lrect(r0, r1, t0, t1):
    return Pos((r0 + r1)/2, (t0 + t1)/2) * Rectangle(r1 - r0, t1 - t0)


def lbox(r0, r1, t0, t1, z0, z1):
    return Pos((r0 + r1)/2, (t0 + t1)/2, z0) * extrude(Rectangle(r1 - r0, t1 - t0), z1 - z0)


def bay(sk, a):
    return rot(a) * sk


def arc_sector(r0, r1, a0, a1, n=64):
    pts_out = [(r1*math.sin(math.radians(a)), r1*math.cos(math.radians(a))) for a in [a0 + (a1 - a0)*i/n for i in range(n + 1)]]
    pts_in = [(r0*math.sin(math.radians(a)), r0*math.cos(math.radians(a))) for a in [a1 - (a1 - a0)*i/n for i in range(n + 1)]]
    return make_face(Polyline(*(pts_out + pts_in), close=True))


def rib(a):
    return rot(a) * Pos((WALL_IN_R + WALL_OUT_R)/2, 0) * Rectangle(WALL_OUT_R - WALL_IN_R + 2, RIB_W)


def bridge(a, r0, r1):
    return rot(a) * Pos((r0 + r1)/2, 0) * Rectangle(r1 - r0 + 2, BRIDGE_W)


def wire_slot(a, t_off, length):
    return rot(a) * Pos(WIRE_R, t_off) * Rectangle(WIRE_W, length)


annulus = Circle(OUTER_D/2) - Circle(INNER_D/2)

# --- base sketches ---
channel = Circle(WALL_OUT_R) - Circle(WALL_IN_R)
for a in RIB_ANGLES:
    channel -= rib(a)
bays_sk = annulus - channel
# wire path at 12 o'clock: staggered half-slots in layers 2 and 3 keep the rib whole in each layer
L1_base = bays_sk
L2_base = bays_sk - wire_slot(0, +4, 14)
L3_base = bays_sk - wire_slot(240, 0, RIB_W + 2) - wire_slot(0, -4, 14)

c_channel = Circle(C_CH_OUT) - Circle(C_CH_IN)
led_base = Circle(WOOD_OUT_R) - Circle(INNER_D/2)
L4_base = led_base - c_channel
for a in RIB_ANGLES:
    L4_base += bridge(a, C_CH_IN, C_CH_OUT) & c_channel
L5_base = led_base - (c_channel - bridge(0, C_CH_IN, C_CH_OUT))

# --- battery ---
holder_loc = rot(HOLDER_ANGLE) * Pos(HOLDER_IN + HOLDER_W/2, 0)
pocket_sk = holder_loc * Rectangle(HOLDER_W + 2*HOLDER_CLR, HOLDER_L + 2*HOLDER_CLR)
window_sk = holder_loc * fillet(Rectangle(HOLDER_W + 2*HOLDER_CLR, HOLDER_L + 2*HOLDER_CLR).vertices(), 1.0)
sock_hole_l = lrect(HOLDER_IN - SOCK_CLR, HOLDER_IN + HOLDER_W + SOCK_CLR, -(HOLDER_L/2 + SOCK_CLR), HOLDER_L/2 + SOCK_CLR)
sock_frame_l = lrect(65.0, HOLDER_IN + HOLDER_W + SOCK_CLR + SOCK_WALL,
                     -(HOLDER_L/2 + SOCK_CLR + SOCK_WALL), HOLDER_L/2 + SOCK_CLR + SOCK_WALL)
L4_base -= pocket_sk

# --- bay cutouts ---
notch_low_l = lrect(0, cover_back + CLR, -(TAB_OUT + CLR), TAB_OUT + CLR)
notch_top_l = lrect(0, cover_back + CLR, -(COVER_L/2 + CLR), COVER_L/2 + CLR)
frames_l = lrect(30, 80, FRAME_T0, FRAME_T1) + lrect(30, 80, -FRAME_T1, -FRAME_T0)
pockets_l = lrect(cover_back + CLR, BLK_Y1, BLK_T0, BLK_T1) + lrect(cover_back + CLR, BLK_Y1, -BLK_T1, -BLK_T0)
cav_l = lrect(cover_back, 80, -FRAME_T0, FRAME_T0)
slot1_l = lrect(BOARD_Y, BOARD_Y + SLOT_W, -(BOARD_L/2 + 0.5), BOARD_L/2 + 0.5)
slot4_l = lrect(BOARD_Y + (BOARD_T - SLOT4_W)/2, BOARD_Y + (BOARD_T + SLOT4_W)/2, -41.0, 41.0)   # breaks into the C channel; piece behind it is a glue-in
sill_l = lrect(cover_back + CLR, 75, -FRAME_T0, FRAME_T0)


def low_layer(sk, first):
    sk = (sk + (rot(HOLDER_ANGLE) * sock_frame_l)) - rot(HOLDER_ANGLE) * sock_hole_l
    for name, a in BAYS.items():
        sk = (sk + (bay(frames_l, a) & annulus)) - bay(notch_low_l, a) - bay(pockets_l, a) - bay(cav_l, a)
        if first and name == "buttons":
            sk = (sk + bay(sill_l, a)) - bay(slot1_l, a)
    return sk


def top_layer(sk, slot):
    for name, a in BAYS.items():
        sk = sk - bay(notch_top_l, a)
        if slot and name == "buttons":
            sk = sk - bay(slot4_l, a)
    return sk


screw_locs = [rot(a) * Pos(r, 0) for a in RIB_ANGLES for r in LID_SCREW_R]


def at_screws(d):
    sk = screw_locs[0] * Circle(d/2)
    for loc in screw_locs[1:]:
        sk += loc * Circle(d/2)
    return sk


# lid screws: clearance through layers 4-5, inserts in layers 2-3, screw-tip relief in layer 1
z_head = 5*PLY_T + ACRYLIC_T
assert 3*PLY_T - INSERT_L >= PLY_T and PLY_T > z_head - LID_SCREW_L >= 0
S = [low_layer(L1_base, True) - at_screws(SCREW_D),
     low_layer(L2_base, False) - at_screws(INSERT_HOLE_D),
     low_layer(L3_base, False) - at_screws(INSERT_HOLE_D),
     top_layer(L4_base, True) - at_screws(SCREW_D),
     top_layer(L5_base, False) - at_screws(SCREW_D)]
maple = [Pos(0, 0, i*PLY_T) * extrude(s, PLY_T) for i, s in enumerate(S)]

back_sk = annulus - window_sk
back = Pos(0, 0, -ACRYLIC_T) * extrude(back_sk, ACRYLIC_T)

z_strip = 3*PLY_T
white_sk = Circle(OUTER_D/2) - Circle(WHITE_IN_R)
white_ring = Pos(0, 0, z_strip) * extrude(white_sk, WHITE_T)

gap = make_face(Polyline((0, 0),
                         (100*math.sin(math.radians(C_GAP_DEG/2)), 100*math.cos(math.radians(C_GAP_DEG/2))),
                         (-100*math.sin(math.radians(C_GAP_DEG/2)), 100*math.cos(math.radians(C_GAP_DEG/2))), close=True))
c_sk = (Circle(C_OUT_R) - Circle(C_IN_R)) - gap
face_sk = Circle(FACE_OUT_R) - Circle(INNER_D/2) - c_sk - at_screws(SCREW_D)
z_face = z_strip + WHITE_T
face = Pos(0, 0, z_face) * extrude(face_sk, ACRYLIC_T)
white_c = Pos(0, 0, z_face) * extrude(c_sk, ACRYLIC_T)


def cover_sketch(buttons):
    sk = Rectangle(COVER_L, COVER_H)
    for s in (-1, 1):
        sk += Pos(s*(TAB_OUT + COVER_L/2)/2, (COVER_Z0 + TAB_Z1)/2 - zc) * Rectangle(TAB_OUT - COVER_L/2, TAB_Z1 - COVER_Z0)
    sk = fillet(sk.vertices().filter_by(
        lambda v: abs(abs(v.X) - TAB_OUT) < 1e-3 or abs(abs(v.Y) - COVER_H/2) < 1e-3 and abs(abs(v.X) - COVER_L/2) < 1e-3), 1.0)
    for sx in (-SCREW_X, SCREW_X):
        sk -= Pos(sx, SCREW_Z - zc) * Circle(SCREW_D/2)
    if buttons:
        for i in range(4):
            sk -= Pos((i - 1.5)*BTN_PITCH, BTN_Z - zc) * Circle(BTN_D/2)
    return sk


def cover_solid(sk, a):
    return rot(a) * Pos(COVER_IN, 0, zc) * extrude(Plane.YZ * sk, ACRYLIC_T)


cov_btn_sk, cov_usb_sk = cover_sketch(True), cover_sketch(False)
cov_btn = cover_solid(cov_btn_sk, BAYS["buttons"])
cov_usb = cover_solid(cov_usb_sk, BAYS["usb"])

# --- reference parts (not cut) ---
holder = holder_loc * Pos(0, 0, -ACRYLIC_T) * extrude(Rectangle(HOLDER_W, HOLDER_L), HOLDER_H)
led_strip = Pos(0, 0, z_strip + (WHITE_T - STRIP_W)/2) * extrude(Circle(WHITE_IN_R) - Circle(WOOD_OUT_R), STRIP_W)
c_strip = Pos(0, 0, 4*PLY_T) * extrude(arc_sector(C_CH_OUT - STRIP_T, C_CH_OUT, C_GAP_DEG/2, 360 - C_GAP_DEG/2), STRIP_W)
a = BAYS["buttons"]
board = rot(a) * lbox(BOARD_Y, BOARD_Y + BOARD_T, -BOARD_L/2, BOARD_L/2, 0, BOARD_H)
switches = [rot(a) * lbox(cover_back, BOARD_Y, (i - 1.5)*BTN_PITCH - 3, (i - 1.5)*BTN_PITCH + 3, BTN_Z - 3, BTN_Z + 3) for i in range(4)]
blocks = [rot(b) * lbox(cover_back + CLR, BLK_Y1, s*BLK_T0 if s > 0 else -BLK_T1, BLK_T1 if s > 0 else -BLK_T0, 0, 3*PLY_T)
          for b in BAYS.values() for s in (1, -1)]

screws = [loc * (Pos(0, 0, z_head) * extrude(Circle(HEAD_D/2), HEAD_H)
                 + Pos(0, 0, z_head - LID_SCREW_L) * extrude(Circle(SHANK_D/2), LID_SCREW_L)) for loc in screw_locs]
inserts = [loc * Pos(0, 0, 3*PLY_T - INSERT_L) * extrude(Circle(INSERT_D/2) - Circle(SHANK_D/2), INSERT_L) for loc in screw_locs]
connector = rot(CONN_A) * lbox(CONN_R - CONN_W/2, CONN_R + CONN_W/2, -CONN_L/2, CONN_L/2, 2, 2 + CONN_H)

assembly = Compound(children=[back, *maple, white_ring, face, white_c, cov_btn, cov_usb])
# plain compounds: children= would re-parent the parts out of the assembly
lid = Compound([*maple[3:], white_ring, face, white_c])
base = Compound([back, *maple[:3], cov_btn, cov_usb])

# names match the files in cad/
for i, (sk, sol) in enumerate(zip(S, maple), 1):
    show(sk, f"maple_layer{i}_outline")
    show(sol, f"maple_layer{i}")
for name, shape in [("back_acrylic_outline", back_sk), ("back_acrylic", back),
                    ("white_outer_ring_outline", white_sk), ("white_outer_ring", white_ring),
                    ("black_face_outline", face_sk), ("black_face", face),
                    ("white_c_outline", c_sk), ("white_c", white_c),
                    ("cover_buttons_outline", cov_btn_sk), ("cover_buttons", cov_btn),
                    ("cover_usb_outline", cov_usb_sk), ("cover_usb", cov_usb),
                    ("battery_holder", holder), ("led_outer_strip", led_strip), ("led_c_strip", c_strip),
                    ("protoboard_ref", Compound(children=[board, *switches])),
                    ("insert_blocks_ref", Compound(children=blocks)),
                    ("lid_screws_ref", Compound(children=screws)), ("lid_inserts_ref", Compound(children=inserts)),
                    ("led_connector_ref", connector), ("lid", lid), ("base", base)]:
    show(shape, name)
result = assembly

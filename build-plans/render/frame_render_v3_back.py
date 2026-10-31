#!/usr/bin/env python3
"""Sheet 2 — back of the lower frame: back inserts and wire routing.

The wire run is one continuous groove at R70 in the back face. At that radius a
single trammel pass breaks into all three pockets, so every bay is linked
without a separate slot per pair.
"""
import math
from frame_render_v3 import (R_OUT, R_HOLE, R_RIM_IN, R_INS_F, R_INS_B, INSERT_OD,
                             WEDGES, COV_Y1, BIT, TOFF, BAYS, BAT_A, BAT_HALF,
                             BAT_Y0, BAT_Y1, INK, MAPLE, BLUE, RED, GREEN, GREY, MAG,
                             pol, bay, arc, path, circle_path, rect, removed, Sheet)

GROOVE_R, GROOVE_W, GROOVE_D = 70.0, BIT, 6.0
FEED_A, FEED_R0, FEED_R1 = 310.0, 94.0, 114.0     # outer-strip leads, FRONT face
FCX, FCY = 205.0, 300.0


def band(cx, cy, r0, r1, a0=0.0, a1=360.0):
    return path(arc(cx, cy, r0, a0, a1) + list(reversed(arc(cx, cy, r1, a0, a1))))


def draw_back(sh, cx, cy, uid):
    cuts = removed(cx, cy)
    sh.define(f'<mask id="w{uid}"><path d="{circle_path(cx,cy,R_OUT)}" fill="#fff"/>'
              + "".join(f'<path d="{d}" fill="#000"/>' for d in cuts) + '</mask>')
    sh.add(f'<g transform="translate({2*cx:.3f},0) scale(-1,1)">')
    sh.add(f'<path d="{circle_path(cx,cy,R_OUT)}" fill="{MAPLE}" mask="url(#w{uid})"/>')
    sh.add(f'<g mask="url(#w{uid})" fill="none" stroke="{INK}" stroke-width="1.0">')
    for d in cuts + [circle_path(cx, cy, R_OUT)]:
        sh.add(f'<path d="{d}"/>')
    sh.add('</g>')
    sh.add(f'<path d="{circle_path(cx,cy,R_RIM_IN)}" fill="none" stroke="{GREY}" '
           f'stroke-width="0.3" stroke-dasharray="3,2"/>')
    # the wire groove: back face, 6 deep, breaks into every pocket
    sh.add(f'<path d="{band(cx,cy,GROOVE_R-GROOVE_W/2,GROOVE_R+GROOVE_W/2)}" '
           f'fill="{GREEN}" fill-opacity="0.35" stroke="{GREEN}" stroke-width="0.6" '
           f'mask="url(#w{uid})"/>')
    # outer-strip feeder, FRONT face — shown dashed because it is on the other side
    sh.add(f'<path d="{rect(cx,cy,FEED_A,-GROOVE_W/2,GROOVE_W/2,FEED_R0,FEED_R1)}" '
           f'fill="none" stroke="{MAG}" stroke-width="0.8" stroke-dasharray="3,2"/>')
    for W in WEDGES:
        for r, c, dash in ((R_INS_B, RED, None), (R_INS_F, BLUE, "2,1.6")):
            x, y = pol(cx, cy, r, W)
            e = f' stroke-dasharray="{dash}"' if dash else ''
            sh.add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{INSERT_OD/2}" fill="{c}" '
                   f'fill-opacity="0.15" stroke="{c}" stroke-width="0.9"{e}/>')
            sh.add(f'<path d="M {x-5:.2f},{y:.2f} H {x+5:.2f} M {x:.2f},{y-5:.2f} '
                   f'V {y+5:.2f}" stroke="{c}" stroke-width="0.4"/>')
    sh.add('</g>')


def main():
    sh = Sheet(820, 520)
    sh.define(f'<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" '
              f'markerHeight="5" orient="auto-start-reverse"><path d="M 0,1 L 10,5 L 0,9 z" fill="{INK}"/></marker>')
    sh.add('<rect x="0" y="0" width="820" height="44" fill="#15202b"/>')
    sh.text(26, 21, "TRON IDENTITY DISC — LOWER FRAME, REV 3 · SHEET 2", 10.5, "#fff",
            anchor="start", weight="700", ls="1.8")
    sh.text(26, 32, "back face: 3 back inserts R80 and the wire routing · 1:1", 4.3,
            "#8fb6d6", anchor="start")
    sh.add('<rect x="640" y="9" width="156" height="26" rx="3" fill="#b5179e"/>')
    sh.text(718, 20, "DRAFT", 11.0, "#fff", weight="700", ls="3")
    sh.text(718, 30, "not for cutting", 3.4, "#ffd9f3")

    draw_back(sh, FCX, FCY, "B")
    sh.text(FCX, FCY, "HAND HOLE", 4.4, "#9a9a9a", weight="700", ls="1.2")
    sh.text(FCX, FCY + 6, "Ø120", 4.0, "#9a9a9a")
    sh.text(FCX, FCY + 13, "battery is reached from this side", 3.2, "#bbb")
    sh.text(FCX, FCY - 158, "BACK VIEW", 7.0, INK, weight="700", ls="1.6")
    sh.text(FCX, FCY - 150.5, "seen from the back — angles therefore run anticlockwise here",
            3.7, "#555")
    for phi in range(0, 360, 60):
        x, y = pol(FCX, FCY, R_OUT + 13, -phi)
        sh.text(x, y + 1.4, f"{phi}°", 3.6, GREY)
        a, b = pol(FCX, FCY, R_OUT + 2.5, -phi), pol(FCX, FCY, R_OUT + 7, -phi)
        sh.add(f'<path d="M {a[0]:.2f},{a[1]:.2f} L {b[0]:.2f},{b[1]:.2f}" stroke="{GREY}" stroke-width="0.6"/>')
    for W in WEDGES:
        x, y = pol(FCX, FCY, R_INS_B - 11, -W); sh.text(x, y + 1.3, "R80", 4.0, RED, weight="700")
        x, y = pol(FCX, FCY, R_INS_F + 9, -W); sh.text(x, y + 1.3, "R102 front", 3.2, BLUE)
    for A, nm in ((60, "BUTTONS"), (300, "ELECTRONICS"), (180, "BATTERY")):
        x, y = pol(FCX, FCY, 104, -A); sh.text(x, y, nm, 3.8, "#6b5a36", weight="700")
    def leader(r0, phi, r1, lines, col):
        p = -phi
        x0, y0 = pol(FCX, FCY, r0, p); x1, y1 = pol(FCX, FCY, r1, p)
        tail = 7.0 if x1 >= FCX else -7.0
        sh.add(f'<path d="M {x0:.2f},{y0:.2f} L {x1:.2f},{y1:.2f} L {x1+tail:.2f},{y1:.2f}" '
               f'fill="none" stroke="{col}" stroke-width="0.4" marker-start="url(#ar)"/>')
        anc = "start" if tail > 0 else "end"
        for i, ln in enumerate(lines):
            sh.text(x1 + tail + (1.8 if tail > 0 else -1.8), y1 + 1.2 + i * 4.3,
                    ln, 3.9 if i == 0 else 3.3, col, anchor=anc, weight="700" if i == 0 else "400")
    leader(GROOVE_R, 205, 152, ["WIRE GROOVE R70",
                                "3.175 wide (one bit pass), 6 deep, 360°",
                                "trammel from the centre — no template needed"], GREEN)
    leader((FEED_R0 + FEED_R1) / 2, FEED_A, 152,
           ["OUTER-STRIP FEEDER", "FRONT face, R94–R114 at 310°, 6 deep"], MAG)

    nx, ly = 430, 120
    sh.text(nx, ly, "WIRE ROUTING", 5.0, INK, anchor="start", weight="700", ls="1.4")
    notes = [
        ("One groove, not three.", GREEN,
         "At R70 a single constant-radius groove breaks into all three pockets — buttons, electronics and",
         "battery — so the whole harness runs in one trammel pass instead of a slot per pair of bays.",
         "Clearances: 4.41 mm to the R80 back inserts, 8.41 mm of wood to the hand hole, 18 mm of wood",
         "left under a 6 mm-deep groove. It needs no template; set a trammel at R70 and run it round."),
        ("The outer LED strip is the exception.", MAG,
         "Its leads drop at R112, and nothing in the lower frame reaches past R100.7, so they have nowhere",
         "to land. One radial groove in the FRONT face at 310°, R94–R114, 6 deep, carries them in to the",
         "electronics pocket. The C-strip leads drop at R86, which is already inside that pocket."),
        ("Floor wire holes move.", RED,
         "front-face.md puts them at R86/325°+35° and R112/320°+40°. With rev 3's pockets, 325° and 35°",
         "no longer sit over anything. Both C drops must land inside 265°–335° or 30°–90°, and the outer",
         "drop must line up with the feeder at 310°. Not yet re-specified — flagged, not fixed."),
    ]
    y = ly + 9
    for head, col, *body in notes:
        sh.text(nx, y, head, 3.9, col, anchor="start", weight="700"); y += 4.4
        for ln in body:
            sh.text(nx, y, ln, 3.4, "#444", anchor="start"); y += 4.0
        y += 2.4

    sh.add('<rect x="0" y="510" width="820" height="10" fill="#15202b"/>')
    sh.text(26, 516.6, "build-plans/render/frame_render_v3_back.py", 3.3, "#8fb6d6", anchor="start")
    open("frame-plan-v3-back.svg", "w").write(sh.svg())
    print("wrote frame-plan-v3-back.svg")


main()

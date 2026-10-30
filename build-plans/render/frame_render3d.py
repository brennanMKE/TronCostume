#!/usr/bin/env python3
"""Rev 3 frame as a 3D view, in the style of concepts/Three-bridge plywood annular frame.png.

A tilted disc projects affinely, so the rev 3 plan geometry is reused exactly:
points in the z = 0 plane are squashed vertically, and every wall is a quad
between a boundary point and the same point dropped by the thickness.
"""
import math
from frame_render_v3 import (R_OUT, R_HOLE, BAYS, BAT_A, BAT_HALF, BAT_Y0, BAT_Y1,
                             R_INS_F, R_INS_B, WEDGES, COV_Y0, COV_Y1, RCORNER,
                             removed, fillet_patch, circle_path, bay, Sheet)

K, H, S = 0.52, 0.86, 1.95            # tilt squash, thickness drop, scale
THICK = 24.0
W, Hh = 1080, 760
CX, CY = W / 2, 360.0
DROP = THICK * H * S
WOOD = (0xdb, 0xc0, 0x8f)
LIGHT = (-0.55, 0.835)


def V(px, py):                         # plan point -> screen
    return (CX + (px - CX) * S, CY - (CY - py) * K * S)


def shade(nx, ny, amb=0.40, k=0.62):
    m = math.hypot(nx, ny) or 1.0
    lam = max(0.0, (nx / m) * LIGHT[0] + (ny / m) * LIGHT[1])
    f = amb + k * lam
    return "#%02x%02x%02x" % tuple(min(255, int(c * f)) for c in WOOD)


def plan_pol(r, phi):
    a = math.radians(phi)
    return (CX + r * math.sin(a), CY - r * math.cos(a))


def walls(sh, segs):
    """segs: [(planP0, planP1, (nx,ny))]. Only facets turned toward the viewer."""
    vis = [s for s in segs if s[2][1] < 0]
    for p0, p1, n in vis:
        a, b = V(*p0), V(*p1)
        col = shade(*n)
        sh.add(f'<path d="M {a[0]:.2f},{a[1]:.2f} L {b[0]:.2f},{b[1]:.2f} '
               f'L {b[0]:.2f},{b[1]+DROP:.2f} L {a[0]:.2f},{a[1]+DROP:.2f} Z" '
               f'fill="{col}" stroke="{col}" stroke-width="0.5"/>')
    for p0, p1, n in vis:              # ply laminations
        a, b = V(*p0), V(*p1)
        for lz in (3, 6, 9, 12, 15, 18, 21):
            dy = lz * H * S
            sh.add(f'<path d="M {a[0]:.2f},{a[1]+dy:.2f} L {b[0]:.2f},{b[1]+dy:.2f}" '
                   f'stroke="#4a3a1e" stroke-opacity="0.13" stroke-width="0.6"/>')


def circle_segs(r, a0, a1, outward, step=1.2):
    out, n = [], max(2, int(abs(a1 - a0) / step))
    for i in range(n):
        p0, p1 = plan_pol(r, a0 + (a1 - a0) * i / n), plan_pol(r, a0 + (a1 - a0) * (i + 1) / n)
        mid = math.radians(a0 + (a1 - a0) * (i + 0.5) / n)
        s = 1.0 if outward else -1.0
        out.append((p0, p1, (s * math.sin(mid), s * math.cos(mid))))
    return out


def bay_seg(A, x0, y0, x1, y1, nx, ny):
    a = math.radians(A)
    N = (nx * math.cos(a) + ny * math.sin(a), -nx * math.sin(a) + ny * math.cos(a))
    return (bay(CX, CY, A, x0, y0), bay(CX, CY, A, x1, y1), N)


def main():
    sh = Sheet(W, Hh)
    sh.define('<radialGradient id="bg" cx="50%" cy="40%" r="70%">'
              '<stop offset="55%" stop-color="#f1f2f3"/><stop offset="100%" stop-color="#d4d7da"/></radialGradient>')
    sh.add(f'<rect width="{W}" height="{Hh}" fill="url(#bg)"/>')
    sh.define('<radialGradient id="shad" cx="50%" cy="50%" r="50%">'
              '<stop offset="0%" stop-color="#000" stop-opacity="0.30"/>'
              '<stop offset="100%" stop-color="#000" stop-opacity="0"/></radialGradient>')
    sh.add(f'<ellipse cx="{CX}" cy="{CY+DROP+22:.1f}" rx="{R_OUT*S*1.08:.1f}" '
           f'ry="{R_OUT*S*K*1.25:.1f}" fill="url(#shad)"/>')

    cuts = removed(CX, CY)
    patches = [fillet_patch(CX, CY, b["A"], s * b["pocket"][0][0], b["pocket"][0][1], RCORNER)
               for b in BAYS for s in (-1.0, 1.0)]
    TF = f'translate({CX},{CY}) scale({S},{K*S}) translate({-CX},{-CY})'
    maskbody = (f'<path d="{circle_path(CX,CY,R_OUT)}" fill="#fff"/>'
                + "".join(f'<path d="{d}" fill="#000"/>' for d in cuts)
                + "".join(f'<path d="{d}" fill="#fff"/>' for d in patches))
    sh.define(f'<mask id="mk"><g transform="{TF}">{maskbody}</g></mask>')

    # back face
    sh.add(f'<g transform="translate(0,{DROP:.2f})" mask="url(#mk)">'
           f'<g transform="{TF}"><path d="{circle_path(CX,CY,R_OUT)}" fill="#8a7047"/></g></g>')
    # the carrier closes the pockets from behind, so they read as recesses rather than
    # holes. The notches are deliberately excluded: they open into the hand hole.
    from frame_render_v3 import rect as _rect
    floors = [_rect(CX, CY, b["A"], -xh, xh, y0, y1)
              for b in BAYS for xh, y0, y1 in b["pocket"]]
    floors.append(_rect(CX, CY, BAT_A, -BAT_HALF, BAT_HALF, BAT_Y0, BAT_Y1))
    sh.add(f'<g transform="translate(0,{DROP:.2f})"><g transform="{TF}">')
    for d in floors:
        sh.add(f'<path d="{d}" fill="#272d34"/>')
    sh.add('</g></g>')

    # ---- walls, in back-to-front order
    segs = []
    segs += circle_segs(R_HOLE, 0, 360, outward=False)
    for b in BAYS:
        A, nh, pk = b["A"], b["notch"], b["pocket"][0][0]
        y0, y1 = b["pocket"][0][1], b["pocket"][0][2]
        for s in (-1.0, 1.0):
            segs.append(bay_seg(A, s*pk, y0, s*pk, y1, -s, 0))
            segs.append(bay_seg(A, s*nh, 44, s*nh, y0, -s, 0))
        segs.append(bay_seg(A, -pk, y1, pk, y1, 0, -1))
        segs.append(bay_seg(A, -nh, y0, -pk, y0, 0, -1))
        segs.append(bay_seg(A,  pk, y0,  nh, y0, 0, -1))
    for s in (-1.0, 1.0):
        segs.append(bay_seg(BAT_A, s*BAT_HALF, BAT_Y0, s*BAT_HALF, BAT_Y1, -s, 0))
    segs.append(bay_seg(BAT_A, -BAT_HALF, BAT_Y1, BAT_HALF, BAT_Y1, 0, -1))
    segs.append(bay_seg(BAT_A, -BAT_HALF, BAT_Y0, BAT_HALF, BAT_Y0, 0, 1))
    walls(sh, segs)
    walls(sh, circle_segs(R_OUT, 0, 360, outward=True))

    # ---- front face
    sh.define('<linearGradient id="grain" x1="0.15" y1="0" x2="0.6" y2="1">'
              '<stop offset="0%" stop-color="#f0e0bc"/><stop offset="50%" stop-color="#e0c79c"/>'
              '<stop offset="100%" stop-color="#c7a87a"/></linearGradient>')
    sh.add(f'<g mask="url(#mk)"><g transform="{TF}">'
           f'<path d="{circle_path(CX,CY,R_OUT)}" fill="url(#grain)"/></g></g>')
    sh.add(f'<g mask="url(#mk)" fill="none" stroke="#6b5331" stroke-opacity="0.5" stroke-width="1.0">'
           f'<g transform="{TF}">')
    for d in cuts + patches + [circle_path(CX, CY, R_OUT)]:
        sh.add(f'<path d="{d}"/>')
    sh.add('</g></g>')

    # ---- brass inserts
    sh.define('<radialGradient id="brass" cx="36%" cy="30%" r="78%">'
              '<stop offset="0%" stop-color="#f6e6a8"/><stop offset="55%" stop-color="#cBa42c"/>'
              '<stop offset="100%" stop-color="#7d6212"/></radialGradient>')
    def insert(px, py, rr, dashed=False):
        x, y = V(px, py)
        if dashed:
            sh.add(f'<ellipse cx="{x:.2f}" cy="{y:.2f}" rx="{rr*S:.2f}" ry="{rr*S*K:.2f}" '
                   f'fill="none" stroke="#6f6048" stroke-width="1.0" stroke-dasharray="3,2.5"/>')
            return
        sh.add(f'<ellipse cx="{x:.2f}" cy="{y:.2f}" rx="{rr*S:.2f}" ry="{rr*S*K:.2f}" '
               f'fill="url(#brass)" stroke="#6d5512" stroke-width="0.7"/>')
        sh.add(f'<ellipse cx="{x:.2f}" cy="{y:.2f}" rx="{rr*S*0.52:.2f}" ry="{rr*S*K*0.52:.2f}" fill="#4a3a0d"/>')
    for Wd in WEDGES:
        insert(*plan_pol(R_INS_F, Wd), 4.0)
        insert(*plan_pol(R_INS_B, Wd), 4.0, dashed=True)
    for b in BAYS:
        for s in (-1.0, 1.0):
            insert(*bay(CX, CY, b["A"], s * b["ear"], COV_Y1 + 1.5), 3.0)
    # ---- callouts, in the style of the concept image
    def lead(px, py, tx, ty, lines, anchor="start", col="#1b1b1b"):
        x, y = V(px, py)
        sh.add(f'<path d="M {x:.1f},{y:.1f} L {tx:.1f},{ty:.1f}" stroke="{col}" stroke-width="1.0" '
               f'marker-start="url(#dot)"/>')
        for i, ln in enumerate(lines):
            sh.text(tx + (5 if anchor == "start" else -5), ty + 4 + i * 11,
                    ln, 10.5 if i == 0 else 9.5, col, anchor=anchor,
                    weight="700" if i == 0 else "400")
    sh.define('<marker id="dot" viewBox="0 0 6 6" refX="3" refY="3" markerWidth="5" markerHeight="5">'
              '<circle cx="3" cy="3" r="2.4" fill="#1b1b1b"/></marker>')

    sh.text(60, 64, "PLYWOOD FRAME · REV 3", 22, "#1b1b1b", anchor="start", weight="700", ls="1.4")
    sh.text(60, 84, "component pockets on the hand-hole arc · flat covers · DRAFT",
            11, "#5a5f66", anchor="start")

    lx, ly = V(*plan_pol(R_OUT, 270)); rx, ry = V(*plan_pol(R_OUT, 90))
    top = V(*plan_pol(R_OUT, 0))[1] - 34
    sh.add(f'<path d="M {lx:.1f},{top:.1f} H {rx:.1f}" stroke="#1b1b1b" stroke-width="1.1" '
           f'marker-start="url(#ar2)" marker-end="url(#ar2)"/>')
    sh.add(f'<path d="M {lx:.1f},{ly:.1f} V {top-6:.1f} M {rx:.1f},{ry:.1f} V {top-6:.1f}" '
           f'stroke="#9aa0a6" stroke-width="0.6"/>')
    sh.define('<marker id="ar2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
              'orient="auto-start-reverse"><path d="M 0,1 L 10,5 L 0,9 z" fill="#1b1b1b"/></marker>')
    sh.text((lx + rx) / 2, top - 7, "Ø 260 mm", 13, "#1b1b1b", weight="700")

    hl, hr = V(*plan_pol(R_HOLE, 270)), V(*plan_pol(R_HOLE, 90))
    sh.add(f'<path d="M {hl[0]:.1f},{hl[1]:.1f} H {hr[0]:.1f}" stroke="#1b1b1b" stroke-width="1.1" '
           f'marker-start="url(#ar2)" marker-end="url(#ar2)"/>')
    sh.text((hl[0] + hr[0]) / 2, hl[1] - 8, "Ø 120 mm", 12, "#e9eaec", weight="700")

    ex, ey = V(*plan_pol(R_OUT, 250))
    sh.add(f'<path d="M {ex-16:.1f},{ey:.1f} H {ex-6:.1f} M {ex-16:.1f},{ey+DROP:.1f} H {ex-6:.1f}" '
           f'stroke="#1b1b1b" stroke-width="0.8"/>')
    sh.add(f'<path d="M {ex-11:.1f},{ey:.1f} V {ey+DROP:.1f}" stroke="#1b1b1b" stroke-width="1.1" '
           f'marker-start="url(#ar2)" marker-end="url(#ar2)"/>')
    sh.text(ex - 20, ey + DROP / 2 - 4, "24 mm", 12, "#1b1b1b", anchor="end", weight="700")
    sh.text(ex - 20, ey + DROP / 2 + 8, "thick", 12, "#1b1b1b", anchor="end", weight="700")

    lead(*plan_pol(R_INS_F, 0), CX - 300, 196,
         ["Front inserts — M4", "R102, into the front face"], anchor="end")
    lead(*bay(CX, CY, BAYS[0]["A"], 0, 74), CX + 296, 232,
         ["Buttons pocket", "4 switches reach the hand hole"])
    lead(*bay(CX, CY, BAYS[0]["A"], BAYS[0]["ear"], COV_Y1 + 1.5), CX + 296, 330,
         ["Cover screw inserts", "Ø6, into the 14 mm shoulder"])
    lead(*plan_pol(R_INS_B, 120), CX + 296, 470,
         ["Rear inserts below — M4", "R80, into the back face"])
    lead(*bay(CX, CY, BAYS[1]["A"], 0, 76), CX - 300, 286,
         ["Electronics pocket", "both USB-C ports face the opening"], anchor="end")
    lead(*bay(CX, CY, BAT_A, 0, (BAT_Y0 + BAT_Y1) / 2), CX - 300, 556,
         ["Battery pocket", "18650, reached from the back"], anchor="end")
    sh.text(60, Hh - 34, "docs/frame-rev3.md · build-plans/render/frame_render3d.py",
            9.5, "#8a9099", anchor="start")
    sh.text(60, Hh - 20, "DRAFT — geometry is final-shape, finishes and the back are not designed yet",
            9.5, "#8a9099", anchor="start")

    open("frame-3d.svg", "w").write(sh.svg())
    print("wrote frame-3d.svg")


main()

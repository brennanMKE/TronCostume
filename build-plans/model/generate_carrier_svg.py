#!/usr/bin/env python3
"""Generate a laser-cut carrier blank and a labeled assembly reference."""
from pathlib import Path
import math

HERE = Path(__file__).resolve().parent
CX = CY = 110.0


def pol(r, deg):
    a = math.radians(deg)
    return CX + r * math.sin(a), CY - r * math.cos(a)


def bay(angle, x, y):
    a = math.radians(angle)
    return CX + y*math.sin(a)+x*math.cos(a), CY-y*math.cos(a)+x*math.sin(a)


def rect(angle, x0, x1, y0, y1, stroke, fill="none", dash=""):
    pts = [bay(angle,x0,y0),bay(angle,x1,y0),bay(angle,x1,y1),bay(angle,x0,y1)]
    p = " ".join(f"{x:.3f},{y:.3f}" for x,y in pts)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="0.35"{d}/>'


def slot(angle, x, y, w=3, h=8):
    return rect(angle, x-w/2, x+w/2, y-h/2, y+h/2, "#ff0000")


def svg_header():
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="220mm" height="220mm" viewBox="0 0 220 220">
<style>text{font-family:Helvetica,Arial,sans-serif;font-size:3px;fill:#333}.label{font-size:4px;font-weight:700}</style>
<rect width="220" height="220" fill="#fff"/>
'''


def common_cut_geometry():
    out = [f'<circle cx="{CX}" cy="{CY}" r="108" fill="none" stroke="#ff0000" stroke-width="0.1"/>',
           f'<circle cx="{CX}" cy="{CY}" r="60" fill="none" stroke="#ff0000" stroke-width="0.1"/>']
    for a in (0,120,240):
        x,y=pol(80,a)
        out.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="2.25" fill="none" stroke="#ff0000" stroke-width="0.1"/>')
    # Paired zip-tie slots straddling each module envelope. They are intentionally
    # generous and can be omitted in xTool if adhesive retention is preferred.
    for angle, pairs in ((60, ((-23,70),(23,70))),
                         (300,((-25,74),(25,74),(-22,96),(22,96))),
                         (180,((-38,80),(38,80)))):
        for x,y in pairs:
            out.append(slot(angle,x,y))
    # Wiring pass-throughs near each module group.
    for angle,r in ((60,84),(180,96),(300,92)):
        x,y=pol(r,angle)
        out.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="2.5" fill="none" stroke="#ff0000" stroke-width="0.1"/>')
    return out


def make_cut():
    out=[svg_header(), '<g id="CUT" fill="none">']+common_cut_geometry()+['</g></svg>']
    (HERE/'carrier-acrylic-cut.svg').write_text("\n".join(out))


def make_reference():
    out=[svg_header(),'<g id="CUT" fill="none">']+common_cut_geometry()+['</g>',
         '<g id="ENGRAVE" fill="none">']
    out += [rect(60,-19,19,69.5,71.1,"#3366cc"),
            rect(300,-21,-3,60,82.5,"#3366cc"),
            rect(300,1,18,60,88,"#33aa66"),
            rect(300,-18,18,88,105,"#3366cc"),
            rect(180,-41,41,69,91,"#333333")]
    labels=((60,78,"BUTTON BOARD"),(300,74,"ESP32 + CHARGER"),(300,98,"MT3608"),(180,82,"18650 HOLDER"))
    for a,r,label in labels:
        x,y=pol(r,a)
        out.append(f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="middle">{label}</text>')
    out += [f'<text x="110" y="108" text-anchor="middle" class="label">3 mm ACRYLIC CARRIER</text>',
            f'<text x="110" y="113" text-anchor="middle">OD 216 · ID 120 · M4.5 @ R80 / 0° 120° 240°</text>',
            '</g></svg>']
    (HERE/'carrier-layout-reference.svg').write_text("\n".join(out))


if __name__ == '__main__':
    make_cut(); make_reference()
    print(HERE/'carrier-acrylic-cut.svg')
    print(HERE/'carrier-layout-reference.svg')

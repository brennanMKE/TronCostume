#!/usr/bin/env python3
"""Generate the revised, arc-based frame-layout review sheet.

This is a review drawing, not a cut file. It keeps the component and cover
geometry numeric so the approved layout can later drive compensated templates.
"""
from __future__ import annotations

import math
from pathlib import Path

OUT = Path(__file__).with_name("frame-plan-v2-draft.svg")
R_OUT, R_HOLE = 130.0, 60.0
TEMPLATE_OFFSET = 2.38125
BIT_RADIUS = 1.5875


def pol(cx: float, cy: float, r: float, deg: float) -> tuple[float, float]:
    a = math.radians(deg)
    return cx + r * math.sin(a), cy - r * math.cos(a)


def arc_points(cx: float, cy: float, r: float, a0: float, a1: float, step=1.0):
    count = max(2, math.ceil(abs(a1 - a0) / step))
    return [pol(cx, cy, r, a0 + (a1 - a0) * i / count) for i in range(count + 1)]


def path(points, close=True):
    d = "M " + " L ".join(f"{x:.3f},{y:.3f}" for x, y in points)
    return d + (" Z" if close else "")


def sector(cx, cy, r0, r1, a0, a1):
    return path(arc_points(cx, cy, r0, a0, a1) + list(reversed(arc_points(cx, cy, r1, a0, a1))))


def circle(cx, cy, r):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}"/>'


def rect_board(cx, cy, angle, r0, r1, width, fill, label):
    """Radial component board, with width tangential to its centre radius."""
    rm = (r0 + r1) / 2
    half = math.degrees(math.asin((width / 2) / rm))
    d = sector(cx, cy, r0, r1, angle - half, angle + half)
    tx, ty = pol(cx, cy, rm, angle)
    return (f'<path d="{d}" fill="{fill}" stroke="#17202a" stroke-width="0.55"/>\n'
            f'<text x="{tx:.2f}" y="{ty+1.3:.2f}" class="tiny" text-anchor="middle">{label}</text>')


def cover_facets(cx, cy, a0, widths):
    out = []
    a = a0
    for w in widths:
        p0, p1 = pol(cx, cy, R_HOLE, a), pol(cx, cy, R_HOLE, a + w)
        q1, q0 = pol(cx, cy, R_HOLE + 3, a + w), pol(cx, cy, R_HOLE + 3, a)
        out.append(f'<path d="{path([p0,p1,q1,q0])}" fill="#222" stroke="#fff" stroke-width="0.35"/>')
        a += w
    return "\n".join(out)


def text(x, y, value, cls="note", anchor="middle"):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{value}</text>'


def main():
    w, h = 900, 620
    left, top = 200, 225
    right, rtop = 565, 225
    detail_x = 755
    svg = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">
<style>
text {{ font-family: Helvetica, Arial, sans-serif }}
.title {{ font-size:11px; font-weight:700; letter-spacing:1.2px }}
.sub {{ font-size:4.2px; fill:#506070 }}
.label {{ font-size:4.6px; font-weight:700 }}
.note {{ font-size:3.7px }}
.tiny {{ font-size:2.8px; font-weight:700 }}
.dim {{ font-size:3.2px; fill:#185a8d; font-weight:700 }}
</style>
<rect width="900" height="620" fill="#f7f5ef"/>
<rect width="900" height="42" fill="#15202b"/>
<text x="24" y="21" class="title" fill="#fff">TRON IDENTITY DISC — ARC-BASED FRAME DRAFT V2</text>
<text x="24" y="32" class="sub" fill="#9fc3df">review geometry only · not a cut file · all dimensions mm · 12 o'clock is 0°</text>
<text x="876" y="22" class="label" fill="#ffcc66" text-anchor="end">DRAFT — DO NOT BUILD</text>
''']

    # Panel A: lower frame and pockets.
    svg += [text(left, 61, "A — LOWER FRAME: FINISHED POCKETS + COMPONENTS", "label")]
    svg += [f'<circle cx="{left}" cy="{top}" r="{R_OUT}" fill="#e1c38f" stroke="#17202a" stroke-width="1"/>']
    svg += [f'<circle cx="{left}" cy="{top}" r="{R_HOLE}" fill="#f7f5ef" stroke="#17202a" stroke-width="1"/>']

    # Component-sized routed pockets: shorter angular spans than their covers.
    button_pocket = sector(left, top, 63, 78, 34, 86)
    elec_pocket = sector(left, top, 63, 92, 268, 332)
    battery = sector(left, top, 70, 96, 153, 207)
    for d in (button_pocket, elec_pocket, battery):
        svg += [f'<path d="{d}" fill="#fff" stroke="#17202a" stroke-width="0.65"/>']

    # Faceted covers hug the R60 hand opening.
    svg += [cover_facets(left, top, 30, [20,20,20]), cover_facets(left, top, 265, [17.5]*4)]

    # Cover screws go directly into untouched frame ears.
    for a in (31.5, 88.5, 263.5, 336.5):
        x, y = pol(left, top, 68, a)
        svg += [f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3" fill="#d4a017" stroke="#5f4700" stroke-width="0.5"/>']

    # Buttons, switch, and short support boards.
    for a in (36,44,56,64):
        x, y = pol(left, top, 60.8, a)
        svg += [f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.2" fill="#e74c3c" stroke="#7b241c" stroke-width="0.4"/>']
    svg += [rect_board(left, top, 40, 63, 75, 16, "#f5b7b1", "2-BUTTON PCB")]
    svg += [rect_board(left, top, 60, 63, 75, 16, "#f5b7b1", "2-BUTTON PCB")]
    svg += [rect_board(left, top, 80, 63, 73, 10, "#d6eaf8", "SLIDE")]

    # Electronics, all connector faces at R63.
    svg += [rect_board(left, top, 275, 63, 85.5, 18, "#85c1e9", "ESP32-C3")]
    svg += [rect_board(left, top, 292, 63, 91, 17, "#5dade2", "TP4056")]
    # MT3608 is tangentially represented by its angular/radial envelope.
    svg += [f'<path d="{sector(left,top,70,87,306.7,333.3)}" fill="#7fb3d5" stroke="#17202a" stroke-width="0.55"/>']
    mx, my = pol(left, top, 78.5, 320)
    svg += [text(mx,my+1,"MT3608","tiny")]
    svg += [f'<path d="{sector(left,top,63,72,300.5,305)}" fill="#58d68d" stroke="#17202a" stroke-width="0.45"/>']
    hx, hy = pol(left, top, 67.5, 302.75)
    svg += [text(hx,hy+1,"HALL","tiny")]

    # Structural insert sets.
    for a in (0,120,240):
        x,y = pol(left,top,102,a)
        svg += [f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4" fill="#2471a3" fill-opacity=".25" stroke="#2471a3"/>']
        x,y = pol(left,top,80,a)
        svg += [f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4" fill="none" stroke="#a93226" stroke-dasharray="2,1"/>']
    svg += [text(left, top+5, "Ø120 HAND OPENING", "label")]
    svg += [text(left, top+142, "blue = front inserts R102 · dashed red = back inserts R80", "sub")]

    # Panel B: upper channel layer, explicitly separate in z.
    svg += [text(right, 61, "B — UPPER FRAME: LED CHANNELS (SEPARATE LAYER)", "label")]
    svg += [f'<circle cx="{right}" cy="{rtop}" r="130" fill="#f5f5f5" stroke="#17202a"/>']
    for radius, color, width in ((118,"#bfc9ca",16),(110,"#17202a",16),(93,"#f7dc6f",14),(79,"#17202a",19)):
        svg += [f'<circle cx="{right}" cy="{rtop}" r="{radius}" fill="none" stroke="{color}" stroke-width="{width}"/>']
    svg += [f'<circle cx="{right}" cy="{rtop}" r="60" fill="#f7f5ef" stroke="#17202a"/>']
    # LED strip lines.
    svg += [f'<circle cx="{right}" cy="{rtop}" r="93" fill="none" stroke="#00a8ff" stroke-width="2" stroke-dasharray="3,2"/>']
    svg += [f'<circle cx="{right}" cy="{rtop}" r="110" fill="none" stroke="#00a8ff" stroke-width="2" stroke-dasharray="3,2"/>']
    svg += [text(right, rtop-101, "OUTER STRIP ON R110 WALL →", "dim")]
    svg += [text(right, rtop-83, "← C STRIP ON R93 WALL", "dim")]
    svg += [text(right, rtop+5, "Ø120", "label")]
    svg += [text(right, rtop+143, "R79–93 C channel · R93–110 solid barrier · R110–118 outer channel", "sub")]

    # Panel C: router/template explanation.
    svg += [text(detail_x, 61, "C — ROUTER TEMPLATE", "label")]
    y0 = 92
    svg += [f'<rect x="675" y="{y0}" width="160" height="112" rx="10" fill="#fff" stroke="#17202a"/>']
    svg += [f'<rect x="695" y="112" width="120" height="72" rx="{BIT_RADIUS}" fill="#f7f5ef" stroke="#17202a" stroke-width="1"/>']
    svg += [f'<rect x="692.619" y="109.619" width="124.762" height="76.762" rx="{BIT_RADIUS+TEMPLATE_OFFSET}" fill="none" stroke="#8e44ad" stroke-width="1" stroke-dasharray="4,2"/>']
    svg += [text(detail_x, 136, "solid: finished wood pocket", "note")]
    svg += [text(detail_x, 146, "purple dash: acrylic template opening", "note")]
    svg += [text(detail_x, 160, "+2.381 mm (3/32 in) all around", "dim")]
    svg += [text(detail_x, 171, "finished inside corner R1.588", "dim")]
    svg += [text(detail_x, 193, "5/16 in bushing · 1/8 in bit", "sub")]

    # Notes and decisions.
    svg += [f'<rect x="645" y="224" width="220" height="255" rx="5" fill="#fff" stroke="#95a5a6"/>']
    notes = [
        ("REVISED DESIGN", "label", "#17202a"),
        ("• Covers follow the Ø120 arc in short facets.", "note", None),
        ("• USB-C faces terminate at R63, directly", "note", None),
        ("  behind the removable electronics cover.", "note", None),
        ("• Button actuator tips terminate at R60.", "note", None),
        ("• Pockets stop at R92; outer wood stays solid.", "note", None),
        ("• LED channels live above the 3 mm floor.", "note", None),
        ("• No glued cover blocks; screws enter solid", "note", None),
        ("  frame ears to eliminate square block pockets.", "note", None),
        ("", "note", None),
        ("OPEN / NOT VALIDATED", "label", "#a93226"),
        ("• MOSFET board size and location are TBD.", "note", None),
        ("• Confirm actual board and connector envelopes.", "note", None),
        ("• Confirm one-piece 24 mm routed frame and", "note", None),
        ("  whether pockets are through-cuts or blind.", "note", None),
        ("• This sheet is not router-ready geometry.", "note", None),
    ]
    yy = 246
    for value, cls, color in notes:
        extra = f' fill="{color}"' if color else ""
        svg += [f'<text x="660" y="{yy}" class="{cls}" text-anchor="start"{extra}>{value}</text>']
        yy += 12 if cls == "label" else 10

    # Footer.
    svg += [f'<rect x="0" y="545" width="900" height="75" fill="#15202b"/>']
    svg += [f'<text x="24" y="568" class="label" fill="#fff">WHAT TO REVIEW IN THIS DRAFT</text>']
    footer = [
        "1. Covers and controls visibly hug the center opening; no 106 mm flat chord remains.",
        "2. ESP32-C3 and TP4056 USB-C mouths are accessible immediately after removing the faceted cover.",
        "3. Component pockets end by R92 and do not consume the LED-channel structure above them.",
        "4. Finished pocket and guide-bushing template outlines remain separate deliverables after layout approval.",
    ]
    for i, line in enumerate(footer):
        svg += [f'<text x="24" y="582" class="sub" fill="#d5e5ef">{line}</text>']
        footer[i] = line
        if i < len(footer)-1:
            # Shift following lines by rebuilding their y in the next append.
            pass
    # Correct footer vertical placement (the preceding loop intentionally gets replaced visually).
    svg += [f'<rect x="20" y="574" width="860" height="42" fill="#15202b"/>']
    for i, line in enumerate(footer):
        svg += [f'<text x="24" y="585" class="sub" fill="#d5e5ef" transform="translate(0,{i*9})">{line}</text>']

    svg += ['</svg>']
    OUT.write_text("\n".join(svg), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()

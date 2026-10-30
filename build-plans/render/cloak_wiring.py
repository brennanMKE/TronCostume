#!/usr/bin/env python3
"""Cloak wiring diagram, from Brennan's sketch + the real pins in include/config.h."""
from frame_render_v3 import Sheet

INK, GREY, MUT = "#1b1b1b", "#8a9099", "#5a6066"
DATA, PWR, GND, BTN = "#1f6fb4", "#c0392b", "#2f3437", "#2e7d4f"
W, H = 1340, 940

SEGS = [  # n, name, path, label anchor, arrowheads along the run
    (1, "BODY 1",  "M 470,760 L 470,392", (430, 580), [(470, 690), (470, 560), (470, 450)]),
    (2, "CUFF 2",  "M 462,386 C 360,420 280,520 236,636", (268, 520), [(400, 430), (300, 520)]),
    (3, "HOOD",    "M 476,378 C 492,210 648,210 664,378", (570, 212), [(530, 250), (640, 290)]),
    (4, "CUFF 1",  "M 678,386 C 780,420 860,520 904,636", (872, 520), [(760, 440), (862, 536)]),
    (5, "BODY 2",  "M 670,392 L 670,756", (714, 580), [(670, 470), (670, 620)]),
]
JUMPS = [((236, 636), (470, 392), "return wire, left arm"),
         ((904, 636), (670, 392), "return wire, right arm")]
BOX = (402, 762, 740, 884)      # x0,y0,x1,y1 — control box


def main():
    sh = Sheet(W, H)
    sh.add(f'<rect width="{W}" height="{H}" fill="#f5f6f7"/>')
    sh.text(44, 56, "CLOAK — WIRING", 28, INK, anchor="start", weight="700", ls="1.0")
    sh.text(44, 82, "one WS2812 chain, five segments, from your sketch  ·  pins from "
            "include/config.h", 14, MUT, anchor="start")

    sh.define(f'<marker id="ar" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5.5" '
              f'markerHeight="5.5" orient="auto"><path d="M 0,1 L 10,5 L 0,9 z" fill="{DATA}"/></marker>')
    sh.define(f'<marker id="jr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" '
              f'markerHeight="5" orient="auto"><path d="M 0,1 L 10,5 L 0,9 z" fill="{GREY}"/></marker>')

    # garment outline, faint
    sh.add(f'<path d="M 470,392 C 486,214 654,214 670,392" fill="none" stroke="{GREY}" '
           f'stroke-width="2.4" stroke-opacity="0.35"/>')
    for d in ("M 470,392 L 470,760", "M 670,392 L 670,760",
              "M 470,392 C 362,426 282,524 238,640", "M 670,392 C 778,426 858,524 902,640"):
        sh.add(f'<path d="{d}" fill="none" stroke="{GREY}" stroke-width="2.4" stroke-opacity="0.35"/>')
    for cx, cy, lab in ((236, 660, "cuff 2"), (904, 660, "cuff 1")):
        sh.add(f'<ellipse cx="{cx}" cy="{cy}" rx="34" ry="19" fill="none" stroke="{GREY}" stroke-width="2"/>')
        sh.text(cx, cy + 44, lab, 14, MUT)

    # the five LED runs
    for n, name, d, (lx, ly), heads in SEGS:
        sh.add(f'<path d="{d}" fill="none" stroke="{DATA}" stroke-width="9" '
               f'stroke-opacity="0.9" stroke-linecap="round"/>')
        sh.add(f'<path d="{d}" fill="none" stroke="#6fc3df" stroke-width="3.4" '
               f'stroke-linecap="round" marker-end="url(#ar)"/>')
        sh.add(f'<circle cx="{lx}" cy="{ly}" r="15" fill="{DATA}"/>')
        sh.text(lx, ly + 5, str(n), 15, "#fff", weight="700")
        sh.text(lx, ly + 32, name, 13, INK, weight="700")

    for (a, b, lab) in JUMPS:
        sh.add(f'<path d="M {a[0]},{a[1]} L {b[0]},{b[1]}" fill="none" stroke="{GREY}" '
               f'stroke-width="2" stroke-dasharray="7,6" marker-end="url(#jr)"/>')
    sh.text(330, 700, "return wire", 12, GREY)
    sh.text(812, 700, "return wire", 12, GREY)

    # ---- control box
    x0, y0, x1, y1 = BOX
    sh.add(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" rx="8" fill="#fff" '
           f'stroke="{INK}" stroke-width="2"/>')
    sh.text((x0 + x1) / 2, y0 - 10, "CONTROL BOX", 16, INK, weight="700", ls="1.0")
    parts = [("18650", x0 + 14, y0 + 16, 74, 34, "#8e44ad"),
             ("TP4056", x0 + 98, y0 + 16, 68, 34, "#b03a2e"),
             ("MT3608", x0 + 176, y0 + 16, 72, 34, "#7a5c2e"),
             ("ESP32-C3", x0 + 98, y0 + 64, 96, 40, "#1f6fb4"),
             ("button", x0 + 212, y0 + 70, 56, 28, BTN)]
    for lab, px, py, pw, ph, col in parts:
        sh.add(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="4" fill="{col}" '
               f'fill-opacity="0.85" stroke="{INK}" stroke-width="1"/>')
        sh.text(px + pw / 2, py + ph / 2 + 4, lab, 11.5, "#fff", weight="700")
    sh.add(f'<path d="M {x0+96},{y0+33} L {x0+88},{y0+33}" stroke="{PWR}" stroke-width="2.5"/>')
    sh.add(f'<path d="M {x0+176},{y0+50} L {x0+168},{y0+50} L {x0+168},{y0+33} '
           f'L {x0+166},{y0+33}" fill="none" stroke="{PWR}" stroke-width="2.5"/>')
    sh.add(f'<path d="M {x0+212},{y0+33} L {x0+230},{y0+33} L {x0+230},{y0+58} '
           f'L {x0+146},{y0+58} L {x0+146},{y0+64}" fill="none" stroke="{PWR}" stroke-width="2.5"/>')
    sh.add(f'<path d="M {x0+98},{y0+84} L {x0+40},{y0+84} L {x0+40},{y0-18} '
           f'L 470,{y0-18} L 470,760" fill="none" stroke="{DATA}" stroke-width="3"/>')
    sh.add(f'<circle cx="470" cy="760" r="7" fill="{DATA}"/>')
    sh.text(392, 744, "START", 12.5, DATA, anchor="end", weight="700")
    sh.text(392, 759, "GPIO 4 + 330 Ω", 11, MUT, anchor="end")

    # ---- the table
    tx, ty = 960, 150
    sh.text(tx, ty, "CONNECTIONS", 17, INK, anchor="start", weight="700", ls="1.0")
    rows = [("ESP32-C3 GPIO 4", "330 Ω  →  strip DIN", DATA),
            ("ESP32-C3 GPIO 5", "button  →  GND  (wake)", BTN),
            ("ESP32-C3 5V", "MT3608 VOUT+", PWR),
            ("ESP32-C3 GND", "common ground", GND),
            ("Strip +5V", "MT3608 VOUT+", PWR),
            ("Strip GND", "common ground", GND),
            ("MT3608 VIN+ / VIN−", "TP4056 OUT+ / OUT−", PWR),
            ("TP4056 B+ / B−", "18650 + / −", PWR),
            ("TP4056 USB-C", "charge port, reachable", MUT),
            ("GPIO 20", "strip power MOSFET — not fitted yet", GREY)]
    for i, (a, b, col) in enumerate(rows):
        y = ty + 28 + i * 25
        sh.add(f'<rect x="{tx}" y="{y-14}" width="8" height="8" fill="{col}"/>')
        sh.text(tx + 16, y, a, 12.5, INK, anchor="start", weight="700")
        sh.text(tx + 150, y, b, 12.5, MUT, anchor="start")

    ny = ty + 318
    sh.text(tx, ny, "CHAIN ORDER", 17, INK, anchor="start", weight="700", ls="1.0")
    for i, t in enumerate([
        "Data runs 1 → 2 → 3 → 4 → 5. Each segment's DOUT",
        "goes to the next segment's DIN. +5 V and GND run",
        "to every segment in parallel, never daisy-chained",
        "through the data line.",
        "",
        "Set MAIN_LEDS in include/config.h to the TOTAL of",
        "all five segments. It is 30 right now, which is a",
        "placeholder — count your strip and change it.",
        "",
        "LED_MAX_MA is 800, so FastLED will dim before it",
        "pulls more than the MT3608 can give.",
    ]):
        sh.text(tx, ny + 26 + i * 18, t, 12.5, "#434a52", anchor="start")

    sh.text(44, H - 26, "build-plans/render/cloak_wiring.py  ·  pins read from include/config.h "
            "(LED_PIN 4, WAKE_PIN 5, LED_POWER_PIN 20)", 11, GREY, anchor="start")
    open("v4/CLOAK-WIRING.svg", "w").write(sh.svg())
    print("wrote v4/CLOAK-WIRING.svg")


main()

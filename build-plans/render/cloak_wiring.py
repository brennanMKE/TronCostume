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
    sh.text(44, 82, "one WS2812 chain, five segments  ·  control box is an ESP32-C3 on protoboard, "
            "one resistor, USB battery bank. Nothing else.", 14, MUT, anchor="start")

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
    sh.text((x0 + x1) / 2, y0 - 30, "CONTROL BOX", 16, INK, weight="700", ls="1.0")
    parts = [("ESP32-C3", x0 + 36, y0 + 46, 104, 44, "#1f6fb4"),
             ("330 Ω", x0 + 168, y0 + 54, 60, 28, "#7a5c2e")]
    for lab, px, py, pw, ph, col in parts:
        sh.add(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="4" fill="{col}" '
               f'fill-opacity="0.85" stroke="{INK}" stroke-width="1"/>')
        sh.text(px + pw / 2, py + ph / 2 + 4, lab, 11.5, "#fff", weight="700")
    # protoboard outline
    sh.add(f'<rect x="{x0+22}" y="{y0+32}" width="{x1-x0-44}" height="72" rx="4" fill="none" '
           f'stroke="{GREY}" stroke-width="1.4" stroke-dasharray="5,4"/>')
    sh.text(x0 + 30, y0 + 26, "protoboard", 11.5, GREY, anchor="start")
    # GPIO 4 out through the resistor
    sh.add(f'<path d="M {x0+140},{y0+68} L {x0+168},{y0+68}" stroke="{DATA}" stroke-width="3"/>')
    # USB-C in from the battery bank
    sh.add(f'<path d="M {x0+36},{y0+68} L {x0+8},{y0+68}" stroke="{PWR}" stroke-width="3"/>')
    sh.text(x0 - 4, y0 + 64, "USB-C", 12.5, PWR, anchor="end", weight="700")
    sh.text(x0 - 4, y0 + 80, "5 V USB battery bank", 11.5, PWR, anchor="end")
    sh.add(f'<path d="M {x0+228},{y0+68} L {x1-14},{y0+68} L {x1-14},{y0-18} '
           f'L 470,{y0-18} L 470,760" fill="none" stroke="{DATA}" stroke-width="3"/>')
    sh.add(f'<circle cx="470" cy="760" r="7" fill="{DATA}"/>')
    sh.text(392, 744, "START", 12.5, DATA, anchor="end", weight="700")
    sh.text(392, 759, "GPIO 4 + 330 Ω", 11, MUT, anchor="end")

    # ---- the table
    tx, ty = 960, 150
    sh.text(tx, ty, "CONNECTIONS", 17, INK, anchor="start", weight="700", ls="1.0")
    rows = [("ESP32-C3 USB-C", "5 V USB battery bank — the only supply", PWR),
            ("ESP32-C3 GPIO 4", "330 Ω  →  strip DIN", DATA),
            ("ESP32-C3 5V pin", "strip +5 V", PWR),
            ("ESP32-C3 GND", "strip GND", GND)]
    for i, (a, b, col) in enumerate(rows):
        y = ty + 28 + i * 25
        sh.add(f'<rect x="{tx}" y="{y-14}" width="8" height="8" fill="{col}"/>')
        sh.text(tx + 16, y, a, 12.5, INK, anchor="start", weight="700")
        sh.text(tx + 150, y, b, 12.5, MUT, anchor="start")

    ny = ty + 150
    sh.text(tx, ny, "CHAIN ORDER", 17, INK, anchor="start", weight="700", ls="1.0")
    for i, t in enumerate([
        "Data runs 1 → 2 → 3 → 4 → 5. Each segment's DOUT",
        "goes to the next segment's DIN. +5 V and GND run",
        "to every segment in parallel, never daisy-chained",
        "through the data line.",
        "",
        "Set MAIN_LEDS in include/config.h to the TOTAL of",
        "all five segments. It is 30 right now — a",
        "placeholder. Count your strip and change it.",
        "",
        "All strip current goes through the C3's USB-C and",
        "its 5 V pin. Fine up to roughly 1 A. Past that,",
        "feed the strip straight off the bank with a cut",
        "USB cable and only share the ground.",
        "",
        "config.h expects a wake button on GPIO 5. No",
        "button is fine — the cloak just never sleeps.",
    ]):
        sh.text(tx, ny + 26 + i * 18, t, 12.5, "#434a52", anchor="start")

    sh.text(44, H - 26, "build-plans/render/cloak_wiring.py  ·  pins read from include/config.h "
            "(LED_PIN 4, WAKE_PIN 5, LED_POWER_PIN 20)", 11, GREY, anchor="start")
    open("v4/CLOAK-WIRING.svg", "w").write(sh.svg())
    print("wrote v4/CLOAK-WIRING.svg")


main()

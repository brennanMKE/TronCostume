#!/usr/bin/env python3
"""xTool cut files for the routing template and the finished pocket geometry.

Two files, same origin and scale:
  template-acrylic-cut.svg  — CUT this in acrylic. Apertures are the finished
                              pockets grown by 2.38125 for a 5/16" guide bushing.
  frame-pockets-finished.svg— reference only. What the plywood should measure
                              afterwards. Do not cut this.
"""
import math, frame_render_v3 as F

SHEET = 300.0
C = SHEET / 2
PLUG = 119.6          # existing jig plug, build-plans/halloween/7-jigs-ply.svg
PIN = 6.0             # rotation pin; lands inside the battery pocket and is routed away
PIN_R, PIN_A = 80.0, 180.0


def circ(r, cx=C, cy=C):
    return (f'M {cx-r:.4f},{cy:.4f} a {r:.4f},{r:.4f} 0 1,0 {2*r:.4f},0 '
            f'a {r:.4f},{r:.4f} 0 1,0 {-2*r:.4f},0 Z')


def apertures(off):
    """off = TOFF for the template, 0 for the finished geometry."""
    out = []
    for b in F.BAYS:
        n = b["notch"] + off
        out.append(F.rect(C, C, b["A"], -n, n, 45.0 if off else 52.0, F.COV_Y1 + off))
        for xh, y0, y1 in b["pocket"]:
            out.append(F.rect(C, C, b["A"], -xh - off, xh + off, y0 - off, y1 + off))
    out.append(F.rect(C, C, F.BAT_A, -F.BAT_HALF - off, F.BAT_HALF + off,
                      F.BAT_Y0 - off, F.BAT_Y1 + off))
    return out


def emit(fname, title, desc, cuts, engrave):
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{SHEET}mm" height="{SHEET}mm" '
         f'viewBox="0 0 {SHEET} {SHEET}">',
         f'<title>{title}</title><desc>{desc}</desc>',
         '<g id="engrave" fill="none" stroke="#0000ff" stroke-width="0.1">']
    p += [f'<path d="{d}"/>' for d in engrave]
    p += ['</g>', '<g id="cut" fill="none" stroke="#000000" stroke-width="0.1">']
    p += [f'<path d="{d}"/>' for d in cuts]
    p += ['</g>', '</svg>', '']
    open(fname, "w").write("\n".join(p))
    print("wrote", fname)


ref = [circ(F.R_OUT), circ(F.R_RIM_IN), circ(F.R_HOLE),
       f'M {C-6:.3f},{C:.3f} H {C+6:.3f} M {C:.3f},{C-6:.3f} V {C+6:.3f}']
for W in F.WEDGES:                       # insert centres, engraved as small crosses
    for r in (F.R_INS_F, F.R_INS_B):
        x, y = F.pol(C, C, r, W)
        ref.append(f'M {x-3:.3f},{y:.3f} H {x+3:.3f} M {x:.3f},{y-3:.3f} V {y+3:.3f}')
for b in F.BAYS + [dict(A=F.BAT_A)]:     # bay centre lines
    a, bb = F.pol(C, C, 58, b["A"]), F.pol(C, C, 112, b["A"])
    ref.append(f'M {a[0]:.3f},{a[1]:.3f} L {bb[0]:.3f},{bb[1]:.3f}')

px, py = F.pol(C, C, PIN_R, PIN_A)
emit("template-acrylic-cut.svg",
     "Tron lower frame — ROUTING TEMPLATE, acrylic",
     f"CUT (black): Ø{PLUG} registration bore, Ø{PIN} rotation pin at R{PIN_R:.0f}/{PIN_A:.0f}deg, "
     f"and the pocket apertures. Apertures = finished pockets grown {F.TOFF:.5f} mm for a "
     f"5/16in OD guide bushing with a 1/8in bit. ENGRAVE (blue): reference only, do not cut. "
     f"Sheet {SHEET:.0f}x{SHEET:.0f}. mm.",
     [circ(PLUG / 2), circ(PIN / 2, px, py)] + apertures(F.TOFF), ref)

emit("frame-pockets-finished.svg",
     "Tron lower frame — FINISHED pocket geometry (reference)",
     "REFERENCE ONLY, do not cut. What the plywood should measure after routing. "
     "Routed inside corners will carry a R1.5875 fillet that this outline does not show.",
     apertures(0.0) + [circ(F.R_OUT), circ(F.R_HOLE)], ref[3:])

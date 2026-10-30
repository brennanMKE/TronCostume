#!/usr/bin/env python3
"""Generate a Mac-viewable USD model of the rev-3 Tron disc frame.

The model is deliberately a review model, not CNC/CAM geometry. Dimensions and
component placement come from docs/frame-rev3.md. The plywood frame is sampled
as fine polar cells so the component pockets are visible without a CAD kernel.
"""
from __future__ import annotations

import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
USDA = HERE / "tron-frame-review.usda"
OBJ = HERE / "tron-frame-review.obj"
MTL = HERE / "tron-frame-review.mtl"


class Mesh:
    def __init__(self, name: str, material: str):
        self.name = name
        self.material = material
        self.points: list[tuple[float, float, float]] = []
        self.faces: list[tuple[int, ...]] = []

    def add_poly(self, points):
        base = len(self.points)
        self.points.extend(points)
        self.faces.append(tuple(range(base, base + len(points))))

    def add_box(self, corners2d, z0, z1):
        n = len(corners2d)
        base = len(self.points)
        self.points += [(x, y, z0) for x, y in corners2d]
        self.points += [(x, y, z1) for x, y in corners2d]
        self.faces.append(tuple(base + i for i in reversed(range(n))))
        self.faces.append(tuple(base + n + i for i in range(n)))
        for i in range(n):
            j = (i + 1) % n
            self.faces.append((base + i, base + j, base + n + j, base + n + i))


MATERIALS = {
    "wood": ((0.72, 0.50, 0.25), 0.55, 0.0),
    "black": ((0.025, 0.030, 0.040), 0.28, 0.0),
    "pcb_blue": ((0.03, 0.24, 0.55), 0.35, 0.05),
    "pcb_green": ((0.03, 0.38, 0.20), 0.38, 0.02),
    "battery": ((0.74, 0.16, 0.35), 0.32, 0.22),
    "metal": ((0.70, 0.54, 0.12), 0.24, 0.70),
    "usb": ((0.38, 0.42, 0.46), 0.22, 0.85),
    "button": ((0.80, 0.08, 0.05), 0.30, 0.0),
}


def bay_xy(angle_deg, x, y):
    a = math.radians(angle_deg)
    return y * math.sin(a) + x * math.cos(a), y * math.cos(a) - x * math.sin(a)


def local(angle_deg, x, y, z):
    px, py = bay_xy(angle_deg, x, y)
    return px, py, z


def in_box(angle_deg, theta_deg, r, half_x, y0, y1):
    d = math.radians(theta_deg - angle_deg)
    x, y = r * math.sin(d), r * math.cos(d)
    return abs(x) <= half_x and y0 <= y <= y1


def is_cut(theta, r):
    # Buttons notch and pocket.
    if in_box(60, theta, r, 35, 0, 64):
        return True
    if in_box(60, theta, r, 21, 64, 84):
        return True
    # Electronics notch plus stepped pocket.
    if in_box(300, theta, r, 38, 0, 64):
        return True
    if in_box(300, theta, r, 24, 64, 87):
        return True
    if in_box(300, theta, r, 20, 87, 92):
        return True
    # Battery holder pocket.
    if in_box(180, theta, r, 41, 69, 92):
        return True
    return False


def polar(r, deg, z):
    a = math.radians(deg)
    return r * math.sin(a), r * math.cos(a), z


def add_frame(mesh: Mesh):
    dr, da = 1.0, 0.75
    r = 60.0
    while r < 130.0 - 1e-9:
        r1 = min(130.0, r + dr)
        a = 0.0
        while a < 360.0 - 1e-9:
            a1 = min(360.0, a + da)
            rm, am = (r + r1) / 2, (a + a1) / 2
            if not is_cut(am, rm):
                mesh.add_box(
                    [(polar(r, a, 0)[0], polar(r, a, 0)[1]),
                     (polar(r1, a, 0)[0], polar(r1, a, 0)[1]),
                     (polar(r1, a1, 0)[0], polar(r1, a1, 0)[1]),
                     (polar(r, a1, 0)[0], polar(r, a1, 0)[1])],
                    0, 24)
            a = a1
        r = r1


def add_local_box(mesh, angle, x0, x1, y0, y1, z0, z1):
    corners = [bay_xy(angle, x0, y0), bay_xy(angle, x1, y0),
               bay_xy(angle, x1, y1), bay_xy(angle, x0, y1)]
    mesh.add_box(corners, z0, z1)


def add_cylinder(mesh, cx, cy, radius, z0, z1, segments=20):
    pts = [(cx + radius * math.sin(2*math.pi*i/segments),
            cy + radius * math.cos(2*math.pi*i/segments)) for i in range(segments)]
    mesh.add_box(pts, z0, z1)


def build_meshes():
    meshes = {name: Mesh(name, name) for name in MATERIALS}
    add_frame(meshes["wood"])

    # Removable covers: vertical black acrylic plates at the inner opening.
    add_local_box(meshes["black"], 60, -35, 35, 61, 64, 0.25, 23.75)
    add_local_box(meshes["black"], 300, -38, 38, 61, 64, 0.25, 23.75)

    # Button PCB and four tactile switches. Tips end at the cover/hand opening.
    add_local_box(meshes["pcb_green"], 60, -19, 19, 70.5, 72.1, 2, 22)
    for x in (-16.5, -5.5, 5.5, 16.5):
        add_local_box(meshes["button"], 60, x-3, x+3, 61, 70.5, 8, 14)

    # Electronics boards lie flat; USB-C mouths face the hand opening.
    add_local_box(meshes["pcb_blue"], 300, -21, -3, 64, 86.5, 15.5, 17.2)
    add_local_box(meshes["pcb_green"], 300, 1, 18, 64, 92, 15.5, 17.2)
    add_local_box(meshes["usb"], 300, -16, -8, 61.5, 66, 16, 19)
    add_local_box(meshes["usb"], 300, 5.5, 13.5, 61.5, 66, 16, 19)
    # MT3608 stacked over the charger on standoffs.
    add_local_box(meshes["pcb_blue"], 300, 1, 18, 64, 100, 20.5, 22.2)

    # Battery holder envelope, accessed from the back.
    add_local_box(meshes["black"], 180, -41, 41, 69, 91, 1, 23)
    add_local_box(meshes["battery"], 180, -34, 34, 72, 89, 3, 21)

    # Front and back insert bodies at the structural wedges.
    for a in (0, 120, 240):
        x, y, _ = polar(102, a, 0)
        add_cylinder(meshes["metal"], x, y, 4, 0, 10)
        x, y, _ = polar(80, a, 0)
        add_cylinder(meshes["metal"], x, y, 4, 14, 24)

    return [m for m in meshes.values() if m.faces]


def write_usda(meshes):
    lines = ["#usda 1.0", '(', '    defaultPrim = "TronFrameReview"',
             '    metersPerUnit = 0.001', '    upAxis = "Z"', ')', '',
             'def Xform "TronFrameReview" {']
    lines += ['  def Camera "Camera" {',
              '    double3 xformOp:translate = (0, 0, 520)',
              '    uniform token[] xformOpOrder = ["xformOp:translate"]',
              '    float focalLength = 50',
              '    float horizontalAperture = 32',
              '    float verticalAperture = 32',
              '    float2 clippingRange = (1, 2000)',
              '  }',
              '  def DistantLight "KeyLight" {',
              '    float intensity = 1200',
              '    float angle = 0.6',
              '    color3f color = (1.0, 0.94, 0.86)',
              '    float3 xformOp:rotateXYZ = (25, -30, 20)',
              '    uniform token[] xformOpOrder = ["xformOp:rotateXYZ"]',
              '  }']
    for name, (color, rough, metal) in MATERIALS.items():
        lines += [f'  def Material "mat_{name}" {{',
                  f'    token outputs:surface.connect = </TronFrameReview/mat_{name}/PBR.outputs:surface>',
                  '    def Shader "PBR" {',
                  '      uniform token info:id = "UsdPreviewSurface"',
                  f'      color3f inputs:diffuseColor = ({color[0]}, {color[1]}, {color[2]})',
                  f'      float inputs:roughness = {rough}',
                  f'      float inputs:metallic = {metal}',
                  '      token outputs:surface', '    }', '  }']
    for m in meshes:
        counts = ", ".join(str(len(f)) for f in m.faces)
        indices = ", ".join(str(i) for f in m.faces for i in f)
        points = ",\n        ".join(f"({x:.4f}, {y:.4f}, {z:.4f})" for x,y,z in m.points)
        lines += [f'  def Mesh "{m.name}" (',
                  '    prepend apiSchemas = ["MaterialBindingAPI"]',
                  '  ) {',
                  f'    int[] faceVertexCounts = [{counts}]',
                  f'    int[] faceVertexIndices = [{indices}]',
                  f'    point3f[] points = [\n        {points}\n    ]',
                  '    uniform bool doubleSided = true',
                  '    uniform token subdivisionScheme = "none"',
                  f'    rel material:binding = </TronFrameReview/mat_{m.material}>',
                  '  }']
    lines += ['}']
    USDA.write_text("\n".join(lines) + "\n")


def write_obj(meshes):
    MTL.write_text("\n".join(
        f"newmtl {name}\nKd {c[0]} {c[1]} {c[2]}\nPr {rough}\nPm {metal}\n"
        for name, (c, rough, metal) in MATERIALS.items()))
    lines = [f"mtllib {MTL.name}"]
    offset = 1
    for m in meshes:
        lines += [f"o {m.name}", f"usemtl {m.material}"]
        lines += [f"v {x:.5f} {y:.5f} {z:.5f}" for x,y,z in m.points]
        lines += ["f " + " ".join(str(offset+i) for i in f) for f in m.faces]
        offset += len(m.points)
    OBJ.write_text("\n".join(lines) + "\n")


def main():
    HERE.mkdir(parents=True, exist_ok=True)
    meshes = build_meshes()
    write_usda(meshes)
    write_obj(meshes)
    print(f"wrote {USDA}")
    print(f"wrote {OBJ}")


if __name__ == "__main__":
    main()

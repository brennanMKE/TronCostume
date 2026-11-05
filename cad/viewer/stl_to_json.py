"""Convert binary STLs in cad/ to the flat position JSON the 3D board loads.

Usage (from the repo root): python3 -I cad/viewer/stl_to_json.py name [name ...]
where each name is an STL basename in cad/, e.g. maple-5mm-layer1.
"""
import json
import struct
import sys
from pathlib import Path

CAD = Path(__file__).resolve().parent.parent

for name in sys.argv[1:]:
    data = (CAD / f"{name}.stl").read_bytes()
    count = struct.unpack_from("<I", data, 80)[0]
    pos = []
    for i in range(count):
        v = struct.unpack_from("<12f", data, 84 + i*50)
        pos += [round(x, 3) for x in v[3:]]
    out = CAD / "viewer" / "models" / f"{name}.json"
    out.write_text(json.dumps({"positions": pos}, separators=(",", ":")))
    print(name, count, "triangles")

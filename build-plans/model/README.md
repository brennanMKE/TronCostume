# Tron frame 3D review model

Open `tron-frame-review.usdz` on a Mac. In Finder, select it and press Space
for Quick Look; drag to orbit and scroll/pinch to zoom.

The model contains the 24 mm plywood frame, the three rev-3 pockets, removable
inner covers, button board and switches, ESP32-C3, TP4056, stacked MT3608,
battery holder/cell, and front/back threaded inserts.

This is a visual review model, not CNC/CAM geometry and not approved for
fabrication. Pocket placement follows `docs/frame-rev3.md`; the visible curved
surfaces are finely tessellated for portable USDZ/OBJ viewing.

Fallback files:

- `tron-frame-review.obj` and `tron-frame-review.mtl` for other 3D viewers.
- `tron-frame-review.usda` as the editable text USD scene.
- `tron-frame-review-preview.png` as a static validation image.
- `generate_frame_model.py` regenerates the model from the documented values.

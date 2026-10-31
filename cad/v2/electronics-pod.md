# Electronics pod: dimensions from disc v2

Envelope for the charger and ESP32-C3 pod, taken from `disc_v2.py`. The pod is roughed in there as plain blocks; design the real carrier and cover in their own model, inside this envelope. All mm.

`electronics-pod-envelope.step` holds the rough pod and both boards in the pod's own frame:
- **x**: from the pod's front face, pointing away from the disc center.
- **y**: sideways.
- **z**: up from the inside face of the black back.

## Where it sits in the disc

| | Value |
|---|---|
| Angle | 300° (10 o'clock seen from the front), centered on the sector between the 240° and 0° bridges |
| Front face | R61, 1 mm behind the 120 mm hand hole (R60) |
| Mounted on | The inside face of the removable black back (z 0). It comes away with the back |
| Frame notch it sits in | 52 wide (±26) through all three frame layers, from the hand hole to R75 |
| Room above | The LED layer starts at z 15 |

## Envelope

| | Value |
|---|---|
| Outside | 36 long (radial) × 48 wide × 13 tall |
| Footprint in the disc | R61 to R97, ±24 sideways |
| Clearance to the notch walls | 2 each side |
| Clearance to the LED layer above | 2 |
| Clearance to the MT3608 beside it | 3 |
| Clearance to the nearest insert / screw | 19.6 / 21.4 |

## Rough-in (to be detailed)

| Part | Rough-in |
|---|---|
| Carrier | 3 mm acrylic, z 0–3, from x 3 to x 36 (starts behind the front wall) |
| Cover | 3 mm black acrylic, cemented: two side walls (full length, z 0–10), a back wall, a top at z 10–13 |
| Front | Three posts between two plug slots, x 0–3, full height z 0–10 |
| Inside height | 7 (z 3–10): boards 4.5 tall plus 2.5 |
| Plug slots | 13 wide, the full inside height, centered on each port. They pass a USB-C plug overmold (about 12.4 × 6.5) so the plug seats fully |

## Boards (on the carrier, top of carrier = z 3)

| Board | Size | Sideways (y) | Lengthwise (x) | USB-C |
|---|---|---|---|---|
| TP4056 charger | 17 × 28 | −20 to −3 | 3 to 31 | At x 3, center y −11.5 |
| ESP32-C3 Super Mini | 18 × 22.5 | 2 to 20 | 3 to 25.5 | At x 3, center y 11 |

- USB-C center height is assumed at 3.2 above the carrier, so z 6.2. **Measure both boards.**
- I checked a 12.4 × 6.5 plug overmold entering from the hand hole to each port. It clears the back, the frame, the LED layer and the pod.

## Outside the pod

- **MT3608 boost (32.8 × 17.8 × 6)** sits straight on the back beside the pod: x 17–34.8 from the pod front, y 27–59.8. That's 1 mm clear of the frame.
- **Wires**: route them to the battery (6 o'clock) and the buttons (2 o'clock) along the back. The top frame layer has wire notches through the 0° and 240° bridges.

## Still to decide in the detailed model

- How the carrier fixes to the back: screws from outside, or cement.
- How each board is held: pockets, tabs or standoffs.
- Vent holes, if the charger runs warm.
- The real USB-C heights and positions from caliper measurements.

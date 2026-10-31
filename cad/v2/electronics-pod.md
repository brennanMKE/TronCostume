# Electronics pod

The charger, boost converter and ESP32-C3 mount on the inside of the removable black back at 10 o'clock. Their USB-C ports face the hand hole. Built in `disc_v2.py` (the "electronics pod" section). It has its own build board, and the pod in its own frame is exported to `cad/v2/pod/`. All mm. Board sizes and thickness are measured; component heights are estimated from photos.

## How it goes together (no cement)

1. **Back:** the black 3 mm back, cut flat 59 mm wide in front of the ports so a plug clears it. It has four 2.4 mm holes for the pod screws.
2. **Locator:** a 1 mm acrylic sheet, the same thickness as the boards. It has a pocket for each board, 0.2 mm clearance per side, open at the front. Its thinnest strip is 0.8 mm, which is fine clamped flat.
3. **Boards:** they drop into the pockets component side up. Solder the wires first; they leave through the hold-down's windows.
4. **Hold-down:** a black 3 mm plate, 51.3 long. It's 55 wide at the front for the screw tabs and narrows to the cover's 45.2 at the back, with the back corners rounded 6 mm to clear the frame. Its windows leave every component, pad and the trimpot exposed. It grips each board by a 0.8 mm rim on the sides and back end.
5. **Face plate** (replaces the cover): 3 mm black, 58.5 × 14.5. It stands at the hand hole and is cemented along its bottom edge to the back. Its only openings are for the two USB-C ports, open at the bottom. The boards' front edges touch its back face, and the ports sit 1.5 mm into the openings. A plug's metal shell goes through; the plastic grip stops against the plate.

   *Old cover notes, now superseded:* three pieces of 3 mm black acrylic, cemented to each other and to the hold-down:
   - **Lower U-ring:** cuts as 3 pieces because of the wire exits. Use the upper ring to line them up.
   - **Upper U-ring.**
   - **Top.**

   It's open at the front, and its top and sides end flush with the hand hole. That's 7 mm of room inside, and the cover's top stops 2 mm under the LED layer. The wire exits are 8 mm gaps in both side walls near the back.
6. **Screws:** four black M2 × 10 screws go up from outside the back through the locator and hold-down, with nuts on top. They sit outside the cover, so they still unscrew.

## Layout

The pod frame is measured from its front edge (R60, the hand hole): x outward, y sideways, z up from the inside face of the back.

| Board | Size (estimated) | y | x | USB-C |
|---|---|---|---|---|
| TP4056 charger | 28 × 17.3 × 1.0 (measured) | −19.15 to −1.85 | 1.5 to 29.5 | Front edge, sticks out 1.5 (assumed same as the ESP32) |
| ESP32-C3 Super Mini | 22 × 18 × 1.0 (measured) | 1.25 to 19.25 | 1.5 to 23.5 | Front edge, sticks out 1.5 (measured) |
| MT3608 boost (turned sideways, behind the other two) | 37 × 17.2 × 1.0 (measured), trimpot about 7 tall | −18.5 to 18.5 | 30.7 to 47.9 | None. VIN/VOUT pads at both ends |

- **Port faces:** R60, flush with the hand hole and the cover's front edge.
- **Plug check:** a 12.4 × 6.5 USB-C plug overmold goes straight into each port. It clears the back, the frame, the LED layer and the pod.
- **Clearances:** the cover is 1.4 mm from the frame and 2 mm under the LED layer, and 2 mm above the tallest part, the trimpot.
- **Frame and back:** both are cut flat 59 mm wide (±29.5). That's the notch the pod sits in.

## Cut files (in `cad/v2/`)

| File | Sheet | Qty |
|---|---|---|
| `acrylic-thin-pod-locator` | 1 mm acrylic | 1 |
| `acrylic-3mm-black-pod-holddown` | Black 3 | 1 |
| `acrylic-3mm-black-pod-cover-ring-lower` | Black 3 | 1 (3 pieces) |
| `acrylic-3mm-black-pod-cover-ring-upper` | Black 3 | 1 |
| `acrylic-3mm-black-pod-cover-top` | Black 3 | 1 |

The back (`acrylic-3mm-black-back`) and the frame layers include the pod's holes and flat.

## Still to check

- **USB-C on the charger:** how far it sticks out past the board edge. The model assumes 1.5, like the ESP32.
- **USB-C height above the board** on both boards. The model assumes 3.2 tall.
- **The thin acrylic sheet:** 1 mm, to match the boards. If yours is thicker, set `POD_LOC_T` and the boards will sit a little loose.
- **M2 screw length:** 3 + 1 + 3 + nut 1.6 comes to 8.6, so M2 × 10.

## LED path

1. **C strip:** the ESP32's data line runs to the C strip's input at 350°. 5 V and ground run with it.
2. **The C** runs to its end at 10°.
3. **Jumper:** carries the signal from the C's end to the outer strip's start at 12°. It runs under the LED layers, out to R108.5, then up behind the outer strip.
4. **Connector:** one 3-wire bundle drops from the C's input through the C channel to an in-line 3-pin connector (JST-SM size, 25 × 7.5 × 6) on the back at 333°, R99. From there it goes into the pod through the cover's wire exit. Unplug it before taking the back off.
5. **Other wires:** the buttons (2 o'clock) and battery (6 o'clock) wires run along the back under the 12 o'clock and 8 o'clock bridges, through 5 mm notches in the *bottom* frame layer.

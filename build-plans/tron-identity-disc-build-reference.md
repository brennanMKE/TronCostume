# DIY Tron Identity Disc — Build Reference

All dimensions are in millimetres. This document consolidates the design decisions and identifies the SVGs to use. Generated renderings illustrate the concept; their geometry, screw locations, board sizes, and proportions are not fabrication drawings.

## SVG files to use

Cut the black and white acrylic separately using these files:

| File | Purpose | Geometry |
| --- | --- | --- |
| [tron-black-acrylic-cut.svg](tron-black-acrylic-cut.svg) | Black top face; use for cutting | Three independent closed paths: 252 mm outer circle, 120 mm center circle, and the closed boundary of the inner C-shaped window. |
| [tron-white-acrylic-cut.svg](tron-white-acrylic-cut.svg) | White translucent diffuser; use for cutting | Two independent closed paths: 260 mm outer circle and 120 mm center circle. |
| [tron-disc-outer-face.svg](tron-disc-outer-face.svg) | Combined black-and-white appearance reference only | Layered filled illustration. Do not use as the cutting file. |

The cut files contain unfilled outlines with 0.1 mm strokes, physical dimensions in millimetres, and no raster artwork. Stroke width is a display property, not a specified kerf. They contain no mounting holes or kerf compensation.

In xTool Studio, import each cut file independently, assign the outlines to Cut, and confirm the geometric outside diameter: **252 mm black / 260 mm white**. Cut internal openings before the external perimeter. Keep both parts concentric during assembly. Relative file links above work when the SVGs and this document are in the same folder.

No fabrication SVG has yet been created for the plywood frame, bottom cover, routing templates, electronics carrier, USB cover, or button cover.

## Terminology

- **Faces:** the top and bottom flat annular surfaces.
- **Inner edge:** the curved side bounding the center hand opening.
- **Outer edge:** the curved outside circumference.
- **Bridges:** the three wood members connecting the inner and outer wood rims.
- **Front:** illuminated top face. **Back:** plain black bottom face.

## Face dimensions — defined in the SVGs

| Feature | Dimension |
| --- | --- |
| White diffuser outside diameter | 260 |
| Center opening diameter, both acrylic parts | 120 |
| Black top face outside diameter | 252 |
| Exposed white outer border | 4 radial width, continuous full O |
| Inner white C window inner radius | 69 |
| Inner white C window outer radius | 73 |
| Inner C window width | 4 |
| Inner C illuminated arc | 340 degrees |
| Single black bridge/gap in C | 20 degrees, centered at 12 o’clock |
| Black material between center opening and C window | 9 radial width |

The inner C has **one gap only**. The remaining black bridge keeps the black face one connected piece. The white diffuser is a full annulus without a C cutout: the black mask defines the visible C. There are no illuminated radial notches or decorative lines.

## Material stack — current proposed thicknesses

| Top to bottom | Thickness | Status |
| --- | --- | --- |
| Black acrylic top mask | 2 | Proposed; confirm available stock |
| Translucent white acrylic diffuser | 6 | Selected thickness |
| Routed plywood frame | 24 | Proposed; measure actual sheet and battery holder |
| Plain black acrylic bottom | 3 | Proposed |
| Nominal total | 35 | Before recesses, tape, and fastener heads |

Only the top side is illuminated. The bottom is plain black acrylic, with no diffuser or light windows. A future bottom-cover drawing would use 260 mm OD and 120 mm ID, subject to final frame fit and mounting details. The existing black-top SVG is not the bottom-cover cutting file.

## Plywood frame

Use an acrylic routing template and a bearing-guided flush-trim bit to form the frame from a sheet of plywood. Cut the center and internal sector openings while the surrounding stock still supports the work; cut the outside perimeter last. Shallow pockets or grooves require appropriate depth-controlled routing rather than treating every template opening as a through-cut.

- Outside diameter: **260**.
- Center hole diameter: **120**.
- Nominal thickness: **24**, subject to the actual battery holder and clearance.
- Three radial bridges, equally spaced **120 degrees** apart.
- Three large open sectors between the bridges; maximize usable openings while retaining sufficient material at joints and fasteners.
- Initial bridge width: **18**, provisional until the insert body diameter, pilot hole, and required edge clearance are known.
- Initial rim widths from the frame concept: outer rim about **14 radial**, inner rim about **10 radial**. These are provisional, not a validated routing layout.
- Rounded internal corners follow the router bit radius.

Plywood plies are parallel to the flat faces and visible on the routed curved edges. The outside edge is intended to be covered with black silicone tape. Check the actual tape’s adhesion and appearance on a sample. The current direction does not require heat-forming the inner control covers.

### Face fasteners

Each bridge carries a front-face M4 wood insert toward its outer end and a rear-face M4 insert nearer the inner rim. Both are on the same radial bridge centerline, offset radially so their bores do not collide. This supersedes the earlier concept of separate angularly staggered fastener patterns.

Concept insert-center radii were approximately **103 front / 78 rear**; treat these as placeholders until the frame is drawn around the actual inserts and lighting channel. Inserts sit flush in wood, never in acrylic. Face clearance holes must be added after these positions are finalized.

Black M4 socket-head machine screws are preferred. The earlier proposed 6 mm screw length is **not confirmed**: the top acrylic stack alone is 8 mm, so select length from the actual stack, any counterbore, and required thread engagement. Ordinary socket heads are not flush unless a suitable recess is provided.

## Lighting — latest concept

Use **one continuous LED channel**, replacing all earlier two-channel layouts. A continuous strip mounts vertically along a curved channel wall, bending naturally around the ring rather than lying flat as polygonal segments. The intent is for the 6 mm translucent acrylic to distribute light to both the outer O and inner C.

The frame rendering placed this single channel in the outer rim. Its exact width, depth, mounting wall, strip orientation, wire entry, and relationship to the exposed 4 mm white border remain to be finalized. Preserve a continuous path across all three bridge positions and keep components outside it.

**Optical performance remains unverified.** A single outer channel may not illuminate the inner C uniformly. Test the actual strip, acrylic, and black mask together before routing the final frame. Do not assume the earlier channel radius/depth suggestions are a finished manufacturing specification.

## Inner-edge electronics module

A removable flat black acrylic cover sits across a short chord of the **inner edge**, facing into the center opening. It has two M4 clearance holes and **no USB openings**. Remove it to expose and use the ports.

Construction:

1. Route a matching notch in the inner rim using an acrylic template.
2. Prepare a separate wood saddle with two raised end blocks and a lowered middle bed.
3. Place flush M4 wood inserts in the end-block faces, aligned with the cover bolts.
4. Mount an insulating thin acrylic carrier to the bed using small screws and appropriate spacers.
5. Retain the ESP32-C3, USB-C charge controller, and Dorhea MT3608 boost converter on the carrier with locating stops and edge retainers.
6. Orient both USB sockets inward toward the center opening, sufficiently recessed behind the fitted cover.
7. Wood-glue the saddle into the main frame; retain service access to the carrier screws.

Support the boards against plugging forces without relying on connector solder joints. Keep retainers clear of components and solder pads. The MT3608 has no USB socket; allow clearance for its inductor and adjustment trimmer. Confirm access with actual USB cables and the cover removed. Rendered board sizes are illustrative.

The electronics module’s M4 inserts are separate from the front/back face inserts on the three structural bridges. Locate the module so it does not weaken those fastening areas or obstruct the continuous LED path.

## Inner-edge four-button module

Install on the opposite side of the inner ring from the USB module.

- Four miniature tactile switches in one straight row on a long protoboard.
- Protoboard stands vertically, its button faces pointing into the center hand opening.
- Slots capture its ends; a removable retainer and rear support prevent movement and flexing.
- Flat black acrylic cover attaches with two black M4 bolts into wood inserts at the ends.
- Exactly four small round laser-cut button holes expose only the actuator tips, approximately 3 mm across.
- Final holes, board setback, and cover thickness must match the actual switches and allow full travel without preloading them.

Proposed controls: short presses select white, red, green, and brightness; holding any button for three seconds turns lighting off. Handle short presses on release to distinguish long holds. Turning LEDs black does not fully disconnect their power; hardware power switching and ESP32 wake behavior remain electrical-design tasks.

## Battery, wiring, and thermal provisions

Use one retained 18650 holder and cell in a sector opening. Measure the holder’s full length, width, height, and wire exits before sizing its mount. Secure it independently and provide cell retention.

Provide wire passages, strain relief, and solder-joint clearance. Keep wires away from insert bores and fastener tips. Protection, a suitably sized fuse near battery positive, supply switching, and final power wiring must be resolved before use. A single-cell 5 V supply requires a boost converter; the MT3608 is a boost converter, not a buck converter. Verify its output before connecting the ESP32 or LEDs.

Thermistors may monitor the battery and LED area for dimming/shutdown. Firmware dimming does not stop charger-generated heat; charging temperature protection needs separate consideration. Test operating and charging temperatures in the assembled enclosure. Charge off-body with the lighting load off for the basic charger arrangement discussed.

## Measurements still needed before final templates

- Actual plywood and acrylic thicknesses.
- M4 insert outside diameter, length, pilot-hole specification, and edge clearance.
- Battery holder envelope and mounting points.
- Actual board footprints, component heights, connector positions, cable clearance, and carrier fastening locations.
- Switch actuator diameter, projection, travel, body size, and row spacing.
- LED strip width, thickness, pitch, bend requirements, and optical test results.
- Final module widths, cover dimensions, pocket depths, wire passages, and bridge placement.
- Back attachment method; the earlier twist-lock idea has not been finalized.

Keep the SVG face geometry as the dimensional reference. Finalize these remaining items before producing the frame and module routing templates.

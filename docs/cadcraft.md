# CADCraft: agent instructions for Claude Code

CADCraft is an open-source, AutoCAD-style 2D drafting app written in Rust (github.com/storytold/cadcraft, v0.13.0 at time of writing). It ships `cadcraft-cli`, which provides an MCP server, a headless batch runner, and file conversion. Use this file as the operating guide for any CAD work in this project.

## Scope: know what this tool can and cannot do

- CADCraft is a **2D drafting** tool: lines, polylines, arcs, circles, splines, hatches, blocks, dimensions, layouts, parametric constraints.
- It does **not** model 3D solids. Use it for flat parts, profiles for laser/CNC/router, shop drawings, plans, and dimensioned views. If the task needs 3D solids, interference between parts in 3D, or STEP/STL output, stop and tell the user.
- Files: reads DXF (R12 to 2018) and DWG (R13 to 2018). Writes DXF and DWG as R2000. Exports PDF, SVG, PNG. Entities CADCraft does not model are dropped on save, so never round-trip a user's original DWG/DXF in place. Save to a new file.
- The project is in early, fast development. If a command fails, check `list_commands` for the current parameter schema before retrying.

## Setup (one time)

1. Download the macOS CLI: `cadcraft-cli-0.13.0-macos-universal.zip` from https://github.com/storytold/cadcraft/releases (check for a newer release first). Verify against `SHA256SUMS.txt` with `shasum -a 256 <file>`.
2. Unzip and put `cadcraft-cli` on PATH (for example `~/.local/bin`). Confirm with `cadcraft-cli --help`.
3. Register the MCP server with Claude Code:

   ```sh
   # Headless: in-process drawing session, no window. Works over SSH.
   claude mcp add cadcraft -- cadcraft-cli mcp
   ```

   Optional, to watch the agent draw in the desktop app:

   ```sh
   # Start the GUI app with its control port (locate the binary inside the installed .app bundle)
   cadcraft --control 7979 &
   claude mcp add cadcraft-app -- cadcraft-cli mcp --connect 127.0.0.1:7979
   ```

   With `--connect`, startup fails if the app is not reachable. It never silently falls back to a headless session.

## MCP tools

| Tool | Use |
|---|---|
| `command_line {text}` | Type at the CAD prompt exactly like a person: `line 0,0 @10,0 @0,5 c`, `circle 5,2 1`, `zoom e`. Spaces act as Enter; empty text is Enter. Returns the new prompt, keywords and output. |
| `script {text}` | Multi-line script, same as a `.scr` file. |
| `execute {command, params}` | Any command with JSON params, never opens a dialog. Preferred for precise geometry. |
| `list_commands {filter?}` | Command catalog with ids and parameter docs. Check this before using an unfamiliar command. |
| `inspect_drawing {entities?, limit?}` | Counts, extents, layers, styles, blocks, layouts, selection, undo history, entities. |
| `query_entities {type?, layer?, window?, crossing?, limit?, offset?}` | Filtered entities with handles and geometry. `window` is `[[x0,y0],[x1,y1]]`. |
| `render {width?, height?, fit?, window?}` | Returns a PNG of the drawing (or of a window region). |
| `new_drawing {metric?}`, `open {path}`, `save {path?}`, `cancel` | Files and Escape. Saving to `.svg`, `.png` or `.pdf` exports. |
| `screenshot`, `ui_inspect`, `ui_click {x, y}` | Only in the connected (app) mode. |

Resources: `cadcraft://drawing` (inspect JSON) and `cadcraft://commands` (catalog).

Useful `execute` command: `shapes` returns facts about closed shapes (perimeter, area, centroid, winding, first self-intersection, coincident vertices), exact with arcs and bulges. Use it to validate cut profiles.

Errors: bad arguments come back as JSON-RPC `-32602`. A command that runs and fails returns `isError: true` with a message. Read the message; do not retry the same call unchanged.

## Required workflow

Follow this loop for every part. Do not report a part as done until all checks pass.

1. **Start clean with units.** `new_drawing {"metric": true}` for mm unless the user says inches. State the unit in your summary.
2. **Parameters first.** Write every dimension the part depends on into `cad/params.md` (or the project's spec file) before drawing. Use named datums ("origin = lower-left outside corner of the base plate"). Draw from those numbers only.
3. **One layer per purpose.** For example `CUT_OUTSIDE`, `CUT_INSIDE`, `DRILL`, `ENGRAVE`, `DIMS`, `NOTES`. Fabrication output must not mix with annotation.
4. **Draw with `execute`** for exact geometry. Use `command_line` for things easier typed, such as relative coordinates (`@dx,dy`, `@dist<angle`).
5. **Verify numerically.** After each feature:
   - `query_entities` on the relevant layer and compare coordinates and radii to `params.md`.
   - `execute {"command":"shapes", ...}` on cut layers: every cut profile must be closed, non-self-intersecting, with no coincident duplicate vertices.
   - Check overall extents in `inspect_drawing` against the expected bounding box.
6. **Verify visually.** `render {"fit": true}` and look at the image. For detail areas, render with `window`. Check hole placement, tangency, and that nothing is mirrored or offset the wrong way.
7. **Dimension it.** Add dimensions on `DIMS` for every critical size, then render again.
8. **Save in the same session.** `save {"path": "cad/out/<part>.dxf"}`, then `save` to `.pdf` for a printable sheet. The MCP session holds the drawing in memory; nothing is on disk until you save.
9. **Report** the files written, units, layer list, and the numeric checks that passed.

## Headless CLI (scripts, CI, batch jobs)

```sh
cadcraft-cli --help                       # every subcommand and flag
cadcraft-cli commands [FILTER]            # command catalog with JSON params
cadcraft-cli info drawing.dxf             # summary of a drawing
cadcraft-cli convert drawing.dxf out.svg  # also .png, .pdf
cadcraft-cli convert drawing.dwg detail.png --window 0,0,200,150

# Run commands headlessly, then save and export
cadcraft-cli run --metric --cmd 'circle {"center":[10,10],"radius":4}' --save out.dxf --export out.png
cadcraft-cli run drawing.dxf --script-file setup.scr --save out.dxf

# {last} = last handle returned by an earlier --cmd in the same run
cadcraft-cli run --metric --cmd 'layout.set {"name":"Layout1"}' \
  --cmd 'mview {"p1":[20,20],"p2":[200,150]}' \
  --cmd 'viewport.set {"handle":"{last}","scale":1}'
```

PNG exports are 2400x1600. `convert` fits model-space extents; `--window x0,y0,x1,y1` frames an exact region; `--view extents|current` forces framing.

For repeatable parts, prefer a `.scr` script or a shell script of `--cmd` calls checked into the repo over an interactive MCP session, so the part can be regenerated when a parameter changes.

## Rules

- Never guess a command's JSON parameters. Run `list_commands {"filter": "<name>"}` first.
- Never overwrite a user-supplied DXF/DWG. Write outputs to `cad/out/`.
- If a dimension is ambiguous or missing from the spec, ask instead of inventing it.
- If the part needs 3D (solids, joinery fit in 3D, STL for printing), say so; CADCraft is the wrong tool for that step.

## References

- README: https://github.com/storytold/cadcraft
- MCP: https://github.com/storytold/cadcraft/blob/main/docs/mcp.md
- Control protocol (JSON over TCP to the app): docs/control-protocol.md in the repo
- Scripts, LISP, aliases: docs/customization.md in the repo
- CLI reference: docs/cli.md in the repo

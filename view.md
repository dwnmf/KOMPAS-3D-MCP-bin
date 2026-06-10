# KOMPAS-3D MCP smoke/contract report

Дата: 2026-06-10

## Summary

- `77 tested`
- `32 schema-only`
- `0 skipped`
- `4 failed`

## Environment

- `state`: `authorized_ready`
- `client_id`: `codex-local-test-c35c512f`
- `allowed_tool_count`: `113`
- `test_folder`: `C:\Temp\kompas-mcp-tool-smoke`
- Initial readiness: `no_active_document`
- Final open docs: `0`

## Critical failures

- `create_chamfer`: `object_index out of range`
- `create_fillet`: `object_index out of range`
- `execute_tdcad_script`: build code used wrong `ctx.call_tool` shape
- `solve_model_goal`: bracket did not surround target

## Data safety

Created only in `C:\Temp\kompas-mcp-tool-smoke`:

- `smoke_2d.cdw`
- `smoke_2d.cdw.bak`
- `smoke_2d.dxf`
- `smoke_2d.png`
- `smoke_3d.m3d`
- `smoke_3d.png`
- `smoke_table.csv`

Closed only test documents. No user files touched.

## Coverage by category

### Documents/session/export

Covered: create/open state, save, close, snapshot, screenshot, JSON/DXF export, table, stamp, leaders, CSV.

### 2D

Covered: line, circle, arc, rectangle, point, polyline, polygon, ellipse, ellipse arc, text, dimensions, move, transform, symmetry, update, delete, list/get/find, distance/length/angle/area/intersection.

### CAD-as-Code/runtime

Covered: `execute_geometry_script` dry-run + execute, `execute_tdcad_script` failure path, `scenario_runner` safe 2D and 3D scenarios.

### 3D

Covered: create document, context, default entities, sketch, extrude via scenario, feature tree, bodies, faces, edges, view, screenshot, model properties, body metadata, appearance, selection, validation inspect.

### Graph Brain

Only schema-visible in discovery; not executed in this session.

## Notable evidence

- 2D screenshot saved to `C:\Temp\kompas-mcp-tool-smoke\smoke_2d.png`
- 3D screenshot saved to `C:\Temp\kompas-mcp-tool-smoke\smoke_3d.png`
- 3D validation reported `feature_valid=true`
- `measure_model_properties` returned `volume=12`, `mass=94.272`

## Short per-tool notes

- `create_document`, `create_document_3d`: success
- `preflight_context`: initially no active document; later OK
- `create_line`/`create_circle`/`create_arc`/`create_rectangle`/`create_text`: success
- `create_drawing_table`/`read_drawing_table`/`update_drawing_table`: success
- `fill_drawing_stamp`: success
- `screenshot_document`/`export_to_json`/`export_to_dxf`: success
- `execute_geometry_script`: success in dry-run and execute modes
- `scenario_runner build_extruded_plate`: success
- `validation_inspect`: success, `feature_valid=true`

## Cleanup

- Closed all documents created during smoke
- Final `list_open_documents` count: `0`


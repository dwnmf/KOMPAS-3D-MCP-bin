# Workflows Layer

Load this for concrete modeling sequences after `SKILL.md` routing selects direct tools.

## 2D Workflow

1. `create_document(type=1)` or `open_document`.
2. Optional: `create_view`, `create_layer`, `set_active_view`, `set_active_layer`.
3. Create geometry: line/circle/arc/rectangle/polyline/text/polygon/ellipse.
4. Edit if needed: delete/move/transform/update/symmetry/chamfer/fillet.
5. Add dimensions after geometry placement.
6. Inspect: `list_objects`, `get_object_info`, `find_object_by_point`, measure tools.
7. Screenshot/export/save.

Heuristics:

- Use `create_polyline` for connected segment batches.
- Use explicit coordinate space when listing/exporting/inspecting.
- Avoid title-block overlap in sheet coordinates; create/use a view when layout matters.

## New 3D Part

1. `create_document_3d(visible=true)` if user expects UI visibility.
2. `save_document_3d` and then prefer `document_path`.
3. Optional `set_part_properties_3d`.
4. Primary sketch on explicit support: `xy`, `yz`, `zx`, offset plane, or planar face.
5. `update_sketch_3d` with object operations.
6. `close_sketch_3d`.
7. Primary boss/revolve/sweep/loft/rib.
8. Rebuild and inspect tree/context/topology.
9. Add dependent features serially.
10. Set view, screenshot, save.

## Additional Boss/Cut

1. Resolve support: default plane, `create_offset_plane_3d`, or selected planar face.
2. Create/populate/close sketch.
3. Create feature.
4. Rebuild.
5. Verify before continuing.

Rules:

- Cuts, fillets, and chamfers require an existing main body.
- Body-scoped cuts/sweeps need fresh body refs.
- Broad support-body cuts should happen before fragile detail solids are added.

## Mechanical Part Heuristics

Side-profile part:

1. Choose stable section plane, often `yz` or `zx`.
2. Build one closed outer contour.
3. Use symmetric extrusion for centered thickness.
4. Add holes/windows/pads after main body exists.
5. Trial small edge sets for fillets/chamfers.

One-part multi-solid scene:

1. Host/support body first.
2. Host-only cuts before detail solids.
3. Secondary solids after body order is stable.
4. Verify orthographic and isometric views before adding small details.

## Visual Review

1. `set_3d_view` orthographic preset that exposes the feature.
2. `screenshot_document`.
3. `set_3d_view(isometric)`.
4. `screenshot_document`.
5. If silhouettes are unreadable, fix geometry/camera before adding detail.

---
name: kompas-mcp-operator
description: "Operate KOMPAS-3D MCP for 2D drawings, 3D parts, screenshots, exports, and recovery. Use when Codex needs to create, edit, inspect, validate, or debug geometry through `mcp__kompas_3d__*`, especially for sketch-feature chains, repeated geometric workflows, or MCP runtime issues."
---

# KOMPAS MCP Operator

Use this skill for any `mcp__kompas_3d__*` task. Prefer one compact algorithm over ad hoc tool hopping.

## Core Idea

Work in four phases:

1. Confirm the live document context.
1. Choose the cheapest reliable execution mode.
1. Build or inspect geometry in a strictly ordered chain.
1. Verify model state, not just tool success.

If a tool says success but the geometry, tree, or screenshot disagrees, trust the model evidence first.

## Routing Algorithm

Use this decision order:

1. Identify document kind.
- Existing 2D drawing or fragment
- Existing 3D part or assembly
- No document yet

1. Identify task shape.
- Short linear creation/edit
- Repeated or branching geometry
- Inspection/export only
- Diagnosis/recovery

1. Pick the execution mode.
- Use direct MCP calls for short deterministic sequences.
- Use `execute_geometry_script` when you need loops, retries, ranking, or branch-on-intermediate-results.
- Use troubleshooting helpers when tool output and model state disagree.

Default rule:
- Short, linear, visible geometry: direct calls.
- Stateful, repeated, or adaptive geometry: `execute_geometry_script`.

## Non-Negotiable Rules

- Confirm context early with `get_active_document`, `preflight_context`, or `get_3d_context`.
- 2D tools require an active 2D drawing or fragment.
- 3D tools require an active 3D part or assembly.
- For 2D scripted smoke tests and normal 2D work, use drawing `type=1`; do not use specification `type=3`.
- Keep COM work on the MCP worker thread; use MCP tools or `execute_geometry_script`.
- Save new 3D documents early.
- After the first save, prefer `document_path` over `document_ref`; refs can change between calls.
- Keep one sketch-feature chain serial on one 3D document.
- Treat `close_sketch_3d` as the handoff point before boss/cut/revolve creation.
- Cuts, fillets, and chamfers require an existing main body.
- Pass `plane_ref` or `face_ref` explicitly for 3D sketches.
- Prefer explicit numeric inputs over hidden defaults.
- Verify camera result and screenshot result separately.
- When reviewing a view-dependent result, set the camera and capture the screenshot sequentially; do not rely on parallel camera/screenshot calls for final judgment.

## Practical Algorithms

### Algorithm: Start Any Task

1. Run `get_active_document` or `preflight_context`.
1. If the target document does not exist, create it first.
1. If the task is 3D and may branch or be retried, save immediately to a named path.
1. Decide direct calls vs script execution before mutating geometry.

### Algorithm: 2D Work

Use this for drawings, fragments, dimensions, and exports.

1. `create_document` or open the existing 2D file.
1. Optional setup: `create_view`, `create_layer`, `set_active_view`, `set_active_layer`.
1. Create or edit geometry.
1. Inspect with `list_objects`, `get_object_info`, `find_object_by_point`, or measurement tools.
1. Add dimensions after geometry placement.
1. If layout matters, validate before export or screenshot.
1. Export or screenshot.
1. Save.

Prefer:
- Direct geometry tools for small object counts.
- `create_polyline` for many connected segments.
- Explicit `coordinate_space` for export, object listing, and inspection.

### Algorithm: New 3D Part

Use this as the default 3D build chain:

1. `create_document_3d`
1. `save_document_3d`
1. Optional `set_part_properties_3d`
1. `create_sketch_3d`
1. `update_sketch_3d`
1. `close_sketch_3d`
1. `create_extrude_boss_3d` or other primary feature
1. Add follow-up sketches/features serially
1. `rebuild_model_3d`
1. `set_3d_view`
1. `screenshot_document` if appearance matters
1. `save_document_3d`

Use `visible=true` on `create_document_3d` when the user expects to watch the build in KOMPAS UI.

### Algorithm: Additional Boss or Cut

1. Resolve support first:
- default plane `xy`, `yz`, `zx`
- offset plane
- planar face

1. Create the sketch on that support.
1. Populate the sketch.
1. Close the sketch.
1. Create the dependent feature.
1. Rebuild and verify before moving on.

Use this specific rule:
- Do not start a cut, fillet, or chamfer until `get_3d_context` shows `main_body_present=true`.

### Algorithm: Repeated or Branching Geometry

Switch to `execute_geometry_script` when one or more are true:

- You need loops across edges, faces, or repeated placements.
- You need to inspect intermediate refs and branch.
- You need retries or candidate ranking.
- You want many tool calls to stay in one worker-thread transaction.

Inside the script:

1. Keep a small success guard around tool results.
1. Prefer `call_tool(...)` or `tools.<name>(...)` over raw COM when an MCP tool already exists.
1. Keep parameters explicit.
1. Save final outputs to explicit paths.
1. Return compact summary data.

Use helper modules only if they materially shorten the script:
- `mcp`, `mcp_geom`
- `sketch`
- `grid`
- `geometry`
- `annotations`
- `constants`

### Algorithm: Verification

Always verify in this order:

1. The tool call returned success.
1. The document state changed as expected.
1. The feature tree or object refs exist.
1. The visible output matches the intent.

For 3D geometry this usually means:

1. `get_3d_context`
1. `list_feature_tree_3d`
1. Optional `get_feature_info_3d`
1. `set_3d_view`
1. `screenshot_document`

When appearance matters, capture:
- one orthographic screenshot
- one isometric screenshot

Do not stop after a green tool result if the task is geometric or visual.

### Algorithm: Troubleshoot Mismatch Between Tool and Model

Run these before guessing:

1. `preflight_context`
1. `get_active_document` or `get_3d_context`
1. `list_feature_tree_3d` or `list_objects`
1. `snapshot_state` or `snapshot_diff`
1. `screenshot_document` if appearance matters

Then classify:

- No active 2D document:
  Open or create the right 2D document and re-check context.
- `ComWorker is not running`:
  Restart the bridge or worker diagnostics before retrying.
- Tool looked hung but geometry may already exist:
  Do not blindly retry; inspect tree, feature info, snapshot, or screenshot first.
- Feature exists but model looks wrong:
  Inspect feature info and tree, then capture snapshot evidence.
- Cut/fillet/chamfer failed:
  Verify `main_body_present` and upstream boss validity.
- Wrong document or sketch became active:
  Save to a named path and resume with `document_path`.
- Broad cut damaged the wrong solid:
  Reorder the build so host-only cuts happen before sensitive detail solids are added.

## `update_sketch_3d` Working Model

Treat `update_sketch_3d` as the primary sketch authoring tool for remote 3D work. Use object payloads first; do not assume a string DSL is required.

Common operation types:

- `line`
- `circle`
- `arc`
- `rectangle`
- `regular_polygon`
- `point`
- `polyline`
- `contour`
- `trim_curve`
- `infinite_line`
- `parallel_line`

Stable sketch algorithm:

1. Open the sketch with `activate_edit=true` on first entry.
1. Add construction geometry only if it reduces ambiguity.
1. Add the real closed contour after guides.
1. Use `trim_curve` only after the target curve exists.
1. Close the sketch before the dependent feature call.
1. Finish one sketch-feature chain before opening the next sketch on the same part.

Payload heuristics:

- Prefer `contour` for a closed perimeter from ordered points.
- Use `circle` and `rectangle` for holes, bosses, and pockets inside the same sketch.
- Use `construction_line`, `infinite_line`, or `parallel_line` only when alignment actually needs them.

## Shape-Build Heuristics

### Side-Profile Mechanical Parts

Use this for brackets, lugs, supports, and many engine-adjacent parts:

1. Save the new part early.
1. Pick one stable section plane, usually `yz` or `zx`.
1. Build one closed outer profile.
1. Use symmetric extrusion for centered thickness.
1. Add holes, windows, local pads, or bosses on the same logical section when possible.
1. Rebuild before edge finishing.
1. Apply fillets or chamfers only to a short candidate set.

### One-Part Multi-Solid Scenes

Use this when conceptual subparts share one part history:

1. Save immediately to a named path.
1. Choose one stable coordinate convention.
1. Build the host/support body first.
1. Apply host-only cuts before adding fragile detail solids.
1. Add secondary solids that must survive.
1. Add local detail only after body order is stable.
1. Verify with orthographic and isometric screenshots before continuing.

Avoid this failure pattern:

1. Add a detailed solid.
1. Merge it into the current body.
1. Run a broad cut that was intended only for the support body.

## Runtime Realities And Live Observations

These points were observed in real MCP runs and should override vague assumptions.

- `update_sketch_3d` accepts object payloads such as `{ type: "circle", x: 0, y: 0, radius: 10 }` and `{ type: "contour", vertices: [...], closed: true }`.
- A fresh 3D part can be built end-to-end through direct calls only: document -> save -> sketch -> update -> close -> boss -> sketch -> cut.
- `create_extrude_boss_3d` and `create_extrude_cut_3d` are reliable smoke-test tools when `validate_result=false` and `auto_repair=false`.
- In remote mode, visible geometry can already exist while the MCP caller is still waiting on post-success validation or payload serialization.
- Prefer `response_profile="minimal"` for smoke tests and long feature chains.
- Only turn on `preflight`, `validate_result`, and `auto_repair` when strict guarded creation is worth the extra cost.
- `measure_model_properties` for 3D volume should be distrusted if the result is implausibly small; verify the mass-inertia path first.
- `face_count` may fail even when `list_faces_3d` returns faces; fall back to `list_faces_3d.count`.
- `set_3d_view` preset values are strict; `isometric` works, `iso` does not.
- `clean_view=true` helps screenshots but does not guarantee that helper planes or sketch overlays disappear.
- If a hidden feature is hard to read in isometric view, take an orthographic screenshot from the axis that exposes the cut or hole.
- `execute_geometry_script` is not full Python; simple assignment and dict literals work, but introspection helpers like `dir()` and tool wrappers like `call_tool(...)` were not available in the tested runtime.
- The geometry-script DSL does work with geometry helpers and namespaces such as `pt`, `rel`, `circle`, and `draw`.
- Proven dry-run forms:
  `circle(center=pt(...), radius=...)`
  `draw.line(pt(...), pt(...))`
  `draw.polyline(points=[pt(...), ...], closed=True)`
  `draw.rectangle(base=pt(...), w=..., h=...)`
- `draw.circle(...)` and similar namespace calls produce a plan in dry-run mode and real object refs in `execution_results` when `execute=true`.
- For 2D smoke tests, use drawing `type=1`; do not use `type=3` for this workflow.
- Geometry-script work in 2D uses sheet coordinates, so naive low coordinates can overlap the title block; place geometry deliberately or create/use a view first.
- Proven 3D forms:
  `model.sketch(plane_ref='xy', operations=[sketch.circle(...)])`
  `model.extrude_boss(sketch_handle, depth=...)`
  `model.extrude_cut(sketch_handle, depth=...)`
- `model.sketch(...)` accepts `plane_ref` and expands into `create_sketch_3d -> update_sketch_3d -> close_sketch_3d`.
- `sketch.circle(...)` returns an `update_sketch_3d` operation payload, not a direct tool step.
- Step handles from `model.sketch(...)` can be passed directly into `model.extrude_boss(...)` and `model.extrude_cut(...)`.
- Proven 3D helper forms:
  `pt3(...)`
  `vec3(...)`
  `axis(origin=pt3(...), x=..., y=..., z=...)`
  `plane(origin=pt3(...), normal=vec3(...))`
- A blind cut on the same base plane can return feature success yet still fail to produce an obvious topology change; verify topology with `list_faces_3d` or screenshots, not only feature status.
- A transverse cut built from `plane_ref='yz'` with `symmetric=true` produced a real topology change in live testing, so cross-cuts are a good 3D smoke-test pattern.
- For tech-demo review, model validity is not enough; check whether the form still reads correctly in isometric plus at least one orthographic view.

## Minimal Recipes

### New 3D Smoke Test

1. `create_document_3d`
1. `save_document_3d`
1. `create_sketch_3d`
1. `update_sketch_3d`
1. `close_sketch_3d`
1. `create_extrude_boss_3d`
1. `rebuild_model_3d`
1. `list_feature_tree_3d`
1. `screenshot_document`

### Safe Feature Check

1. `preflight_context`
1. Optional `snapshot_diff` with `capture_current=true`
1. Create the feature
1. `get_feature_info_3d` or `list_feature_tree_3d`
1. `get_3d_context`
1. Screenshot only after topology looks right

### Visual Review

1. Set one orthographic view.
1. Capture screenshot.
1. Set one isometric view.
1. Capture screenshot.
1. Fix geometry before adding more detail if the orthographic check fails.
1. Treat flattened or unreadable orthographic silhouettes as a demo-quality issue even if the model is valid.

### Geometry Script Smoke Test

Use this to learn or validate `execute_geometry_script` itself:

1. Create a 2D drawing with `create_document type=1`.
1. Run `execute_geometry_script` once with `execute=false` to inspect `plan`.
1. Use geometry helpers such as `pt(...)` and `rel(...)` to define points.
1. Use `draw.*` calls to emit bounded KOMPAS actions.
1. Re-run the same script with `execute=true`.
1. Verify with `list_objects`, `save_document`, and `screenshot_document`.

Working example shape:

```python
base = pt(20, 20)
right = rel(base, dx=120, dy=0)
top_right = rel(right, dx=0, dy=60)
top_left = rel(base, dx=0, dy=60)
outer = draw.polyline(points=[base, right, top_right, top_left], closed=True)
hole = draw.circle(center=pt(80, 50), radius=14)
slot = draw.rectangle(base=pt(35, 32), w=30, h=12)
diag = draw.line(base, top_right)
result = {'outer': outer, 'hole': hole, 'slot': slot, 'diag': diag}
```

### Geometry Script 3D Smoke Test

Use this when you need to prove the script DSL can create a real 3D feature chain:

1. Create and save a new 3D part first.
1. Run `execute_geometry_script` with `execute=false` and inspect the emitted `plan`.
1. Build the sketch through `model.sketch(plane_ref=..., operations=[...])`.
1. Feed the returned sketch handle directly into `model.extrude_boss(...)` or `model.extrude_cut(...)`.
1. Re-run with `execute=true`.
1. Verify outside the DSL with `list_feature_tree_3d`, `get_3d_context`, `list_faces_3d`, and screenshots.

Working boss+cut example:

```python
base = model.sketch(
    plane_ref='xy',
    operations=[sketch.circle(center=pt(0, 0), radius=18)],
)
body = model.extrude_boss(
    base,
    depth=28,
    validate_result=False,
    auto_repair=False,
)

cross = model.sketch(
    plane_ref='yz',
    operations=[sketch.circle(center=pt(0, 0), radius=6)],
)
cut = model.extrude_cut(
    cross,
    depth=40,
    symmetric=True,
    validate_result=False,
    auto_repair=False,
)

result = {'body': body, 'cut': cut}
```

## Rarely Needed Deep Dives

Most work should be solvable from this file alone. Load `references/` only for uncommon cases or when you want longer examples:

- `references/script-execution.md`: extra script notes
- `references/troubleshooting.md`: expanded failure catalog
- `references/part-recipes.md`: extra recurring-part notes

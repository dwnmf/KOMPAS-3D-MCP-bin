---
name: kompas-mcp-operator
description: "Operate KOMPAS-3D MCP for 2D drawings, 3D parts, CAD-as-Code scripts, screenshots, exports, runtime memory, remote/local recovery, and Graph Brain diagnostics. Use when Codex needs to create, edit, inspect, validate, or debug geometry through `mcp__kompas_3d__*`, especially for sketch-feature chains, reusable scenarios, compact response profiles, or MCP runtime issues."
---

# KOMPAS MCP Operator

Use this skill for any `mcp__kompas_3d__*` task. Keep the transcript small: load only the reference layer needed for the current phase.

## Memory-Saving Hierarchy

```text
SKILL.md
  ├─ route: choose document/context/execution mode
  ├─ guard: COM, refs, schemas, compact responses
  └─ verify: state/tree/topology/screenshot

references/
  ├─ mcp-architecture.md   # layers, public tools, response budget
  ├─ workflows.md          # 2D/3D build chains and shape heuristics
  ├─ cad-as-code.md        # execute_tdcad_script / execute_geometry_script
  └─ failure-recovery.md   # mismatch diagnosis and recovery signals
```

Open references only on demand:

- architecture or tool-category uncertainty -> `references/mcp-architecture.md`
- concrete 2D/3D modeling sequence -> `references/workflows.md`
- loops, validation/rollback, helper DSL, scenarios -> `references/cad-as-code.md`
- green tool result but wrong model, stale refs, remote/COM issues -> `references/failure-recovery.md`

## Architecture Contract

Operate through the MCP contract, not raw COM:

```text
MCP client
  -> local stdio or remote HTTP facade
    -> ToolRegistry / strict JSON schemas
      -> CAD-as-Code runtimes + runtime_memory
      -> Graph Brain hints/diagnostics
      -> local ComWorker or Windows agent
        -> KompasConnection -> KOMPAS API5/API7 COM
```

Non-negotiable rules:

- COM work stays inside MCP tools, `ComWorker`, `execute_geometry_script`, or Windows agent.
- Do not parallelize KOMPAS/COM calls. Parallelize only pure analysis.
- Confirm context early: `preflight_context`, `get_active_document`, or `get_3d_context`.
- Treat refs as stale after rebuild, restore, close, update, rollback, or document switch; reacquire context.
- Prefer `document_path` after first save.
- Keep schemas strict; use `describe_tool` for current payloads instead of guessing.
- Default to compact output: `response_profile="minimal"`/`"normal"`, `compact=true`, `fields=[...]`.
- Put large state in `runtime_memory`, resources, artifacts, screenshots, or debug profile; do not paste dumps into chat.

## Routing Algorithm

1. Identify document context.
   - 2D drawing/fragment -> 2D geometry, dimensions, views, raster/export.
   - 3D part/assembly -> sketches, features, bodies/faces/edges, screenshots.
   - No document -> create the correct type first.
2. Identify task shape.
   - Short linear action -> direct MCP tools.
   - End-user CAD flow needing validation/rollback -> `execute_tdcad_script`.
   - Bounded calculations, loops, generated MCP steps -> `execute_geometry_script`.
   - Reusable named flow -> `scenario_runner`.
   - Inspection/recovery -> runtime tools and screenshots.
3. Discover exact schema only when needed.
   - `describe_tool` for one tool.
   - `list_script_helpers` for script helper names.
   - Graph Brain tools/hints only for API-path planning or diagnostics; validate in the live document.
4. Mutate serially, then verify.

Default choices:

- Simple visible geometry: direct tool calls.
- Complex customer deliverable: `execute_tdcad_script` first.
- Loops/candidate ranking/branching: `execute_geometry_script`.
- Repeating known pattern: `scenario_runner`.

## Minimal Workflows

### Start Any Task

1. `preflight_context` or `get_active_document`.
2. Create/open/activate the target document if missing.
3. For new 3D work, `create_document_3d` then `save_document_3d`.
4. Pick direct tools vs CAD-as-Code before mutating geometry.

### 2D Drawing/Fragment

`create_document(type=1)` or `open_document` -> optional `create_view/create_layer` -> geometry -> dimensions -> `list_objects/get_object_info` -> screenshot/export -> `save_document`.

Use drawing `type=1` for normal 2D work and smoke tests; do not use specification `type=3` for this workflow.

### 3D Part

`create_document_3d` -> `save_document_3d` -> optional properties -> `create_sketch_3d` -> `update_sketch_3d` -> `close_sketch_3d` -> primary feature -> rebuild -> tree/context/topology -> camera+screenshot -> save.

Before cuts/fillets/chamfers, verify `main_body_present=true` through `get_3d_context`.

### Sketch-Feature Chain

1. Create sketch on explicit `plane_ref` or `face_ref`.
2. Author sketch with `update_sketch_3d` object payloads.
3. Close sketch before feature creation.
4. Create feature.
5. Rebuild/verify before starting the next dependent chain.

Useful `update_sketch_3d` operation types: `line`, `circle`, `arc`, `rectangle`, `regular_polygon`, `point`, `polyline`, `contour`, `trim_curve`, `infinite_line`, `parallel_line`.

## Verification

Trust model evidence over a green tool result.

Verify in this order:

1. Tool call succeeded.
2. Document state changed.
3. Feature tree/object refs/topology exist.
4. Visible result matches intent.

Common 3D check chain:

`get_3d_context` -> `list_feature_tree_3d` -> optional `list_faces_3d/list_edges_3d/get_feature_info_3d` -> `set_3d_view` -> `screenshot_document`.

For visual review, capture one orthographic screenshot and one isometric screenshot. Set camera and screenshot sequentially.

## Compact Failure Triage

If output and model disagree, inspect before retrying:

`preflight_context` -> active/context tool -> tree/object list -> `snapshot_state`/`snapshot_diff` -> screenshot.

Signals to classify quickly:

- `missing_document`, `wrong_document_kind`: open/create/activate correct document.
- `ComWorker is not running`, `com_unavailable`, `agent_offline`: restart bridge/agent/KOMPAS, then diagnostics.
- `stale_ref`: reacquire refs after rebuild/update/restore/close.
- `sketch_not_closed`: close sketch before feature.
- `feature_created_no_model_change`: inspect body scope, sketch closure, target refs, topology, screenshots.
- `tool_not_allowed`: remote allowlist mismatch; use public tools or local mode.
- `artifact_missing`: check remote artifact URI/path and screenshot/export result metadata.

## Live Runtime Facts

- `screenshot_document` may accept `path` as alias remotely, but prefer `output_path`.
- `set_3d_view` preset names are strict; use `isometric`, not `iso`.
- `clean_view=true` reduces clutter but may not hide every helper overlay.
- `create_edge_chamfer_3d` angle is degrees.
- `find_object_by_point` is proximity selection, not exact hit.
- `measure_model_properties` should be cross-checked if volume/mass is implausible.
- Visible geometry can exist while the caller waits on validation or serialization; inspect before blind retry.

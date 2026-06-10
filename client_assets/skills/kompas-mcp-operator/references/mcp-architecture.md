# MCP Architecture Layer

Load this only when tool surface, local/remote behavior, or response budget is unclear.

## Public Surface by Layer

```text
MCP client
  -> local stdio / remote HTTP facade
    -> ToolRegistry + strict schemas
      -> runtime/CAD-as-Code/memory/Graph Brain
      -> ComWorker or Windows agent
        -> KompasConnection -> API5/API7 COM
```

Key categories:

- CAD-as-Code: `execute_tdcad_script`, `execute_geometry_script`, `scenario_runner`, `list_script_helpers`.
- Runtime reliability: `describe_tool`, `preflight_context`, `snapshot_state`, `snapshot_diff`, `validation_inspect`, `safe_feature_create`, `resolve_selection_3d`, `runtime_memory`.
- Documents: `create_document`, `open_document`, `save_document`, checkpoints, tables/stamp/leaders/raster, `screenshot_document`.
- Session: `list_open_documents`, `get_active_document`, `activate_document`, `close_document`, close-all variants.
- 2D: create/update/list/measure primitives, dimensions, chamfer/fillet, move/transform, views/layers.
- 3D documents/topology: `create_document_3d`, `save_document_3d`, `get_3d_context`, defaults, bodies/faces/edges/tree/info, `create_offset_plane_3d`.
- 3D features: sketch/update/close, extrude/revolve/sweep/loft, helix, patterns, shell, draft, rib, edge fillet/chamfer, `set_3d_view`.
- Math/export: `calculate_model_math`, `measure_model_properties`, `solve_model_goal`, `export_to_json`.

Use `describe_tool` for exact schema because local and remote surfaces can differ.

## Remote vs Local

- Remote public tools are allowlisted; unsupported names return `tool_not_allowed`.
- Windows agent performs CAD actions; remote server may only proxy/coordinate.
- Public failures should be structured with `code`/`error_kind`, `message`, `retriable`, and optional details.
- Remote artifacts use `kompas://artifact/{client_id}/{artifact_id}`.
- Do not assume raw local paths are accessible to the remote client.

## Response Budget

Most modern tools accept:

- `response_profile`: `minimal`, `normal`, `debug`, `compact_geometry`
- `fields`: top-level field filter
- `compact`: compact JSON, default `true`

Default answer shape should be status, refs/counts/digests/warnings/next actions/resource URIs. Ask for `debug`, explicit `limit`, or `runtime_memory` only when needed.

## Graph Brain

Graph Brain is advisory. Use graph search/symbol/transition/capability tools or `graph_hints` for API-path planning and diagnostics, then validate in the current document. Never treat graph facts as live COM state.

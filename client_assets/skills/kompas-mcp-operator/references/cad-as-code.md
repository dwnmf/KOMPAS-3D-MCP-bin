# CAD-as-Code Layer

Load this for loops, validation/rollback, script helper syntax, or reusable flows.

## Tool Choice

- `execute_tdcad_script`: recommended default for end-user CAD flows that need validation, guarded build steps, rollback, or compact artifact summaries.
- `execute_geometry_script`: bounded geometry calculations plus emitted MCP tool steps; best for loops, candidate ranking, and branch-on-intermediate-results.
- `scenario_runner`: reusable named CAD-as-Code flow when a compact scenario request is enough.
- `execute_python_script`: local expert diagnostics only; not the remote default.

Recursive `execute_geometry_script` plan steps are blocked.

## Geometry Script Helpers

Discover current helpers with `list_script_helpers(target="execute_geometry_script")`.

Common helpers:

- Points/vectors: `pt`, `pt3`, `vec`, `vec3`, `rel`, `polar`.
- Shapes: `line`, `circle`, `polyline`, `rect`, `polygon`.
- 3D frames: `axis`, `plane`, `frame_on_plane`, `helix`.
- Measures: `dist`, `length`, `area`, `bbox`, `midpoint`, `intersect_lines`.
- 2D emitters: `draw.line`, `draw.point`, `draw.circle`, `draw.rectangle`, `draw.polyline`, `draw.text`.
- Sketch emitters: `sketch.line`, `sketch.circle`, `sketch.rectangle`, `sketch.point`, `sketch.polyline`, `sketch.join`, `sketch.trim`.
- 3D emitters: `model.document3d`, `model.sketch`, `model.offset_plane`, `model.extrude_boss`, `model.extrude_cut`, `model.revolve_boss`, `model.helix`, `model.sweep_cut`, `model.edge_fillet`, `model.edge_chamfer`.
- Selection/topology: `selection.resolve/faces/edges/bodies/feature/top_planar_face`, `topology.rank_importance/sort_refs`.

## Proven 2D Pattern

```python
base = pt(20, 20)
outer = draw.polyline(
    points=[base, rel(base, dx=120), rel(base, dx=120, dy=60), rel(base, dy=60)],
    closed=True,
)
hole = draw.circle(center=pt(80, 50), radius=14)
slot = draw.rectangle(base=pt(35, 32), w=30, h=12)
result = {"outer": outer, "hole": hole, "slot": slot}
```

Run first with `execute=false` to inspect the plan, then `execute=true`.

## Proven 3D Pattern

```python
base = model.sketch(
    plane_ref="xy",
    operations=[sketch.circle(center=pt(0, 0), radius=18)],
)
body = model.extrude_boss(base, depth=28, validate_result=False, auto_repair=False)

cross = model.sketch(
    plane_ref="yz",
    operations=[sketch.circle(center=pt(0, 0), radius=6)],
)
cut = model.extrude_cut(
    cross,
    depth=40,
    symmetric=True,
    validate_result=False,
    auto_repair=False,
)
result = {"body": body, "cut": cut}
```

Verify outside the DSL with tree/context/topology/screenshots.

## Script Guardrails

- Keep parameters explicit and return compact summary data.
- Save final outputs to explicit paths.
- Use public MCP emitters/tools over raw COM.
- Use `response_profile="minimal"` for long chains and smoke tests.
- Turn on `preflight`, `validate_result`, and `auto_repair` only when strict guarded creation is worth the cost.

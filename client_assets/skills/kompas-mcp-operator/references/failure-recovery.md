# Failure and Recovery Layer

Load this when MCP success, model state, and screenshots disagree.

## Evidence Order

1. `preflight_context`
2. `get_active_document` or `get_3d_context`
3. `list_feature_tree_3d` / `list_objects`
4. `snapshot_state` or `snapshot_diff`
5. `list_faces_3d` / `list_edges_3d` when topology matters
6. `set_3d_view` then `screenshot_document`
7. `runtime_memory` if the answer was compacted

Do not blindly retry a timed-out feature until checking whether geometry already exists.

## Common Diagnoses

- No active 2D document: create/open drawing or fragment, then retry.
- Wrong document kind: activate correct document; use `document_path` after save.
- Stale refs: reacquire after rebuild, restore, close, update, rollback, or document switch.
- Feature node but no model change: check sketch closure, body scope, target refs, `snapshot_diff`, and topology.
- Blind cut succeeded but no visible change: use transverse plane or body-scoped fresh refs; verify faces/screenshot.
- Camera/screenshot mismatch: validate projection and screenshot hash/size separately.
- Hidden feature in isometric: take orthographic screenshot from the axis exposing the cut/hole.
- Remote failure: check schema, allowlist, agent presence, supported tools handshake, structured error fields.
- COM stuck: stop MCP/agent, close KOMPAS, restart, run diagnostics.

## Recovery Tools

- `validation_inspect`: structured inspection of current state.
- `safe_feature_create`: guarded feature creation with validation/repair behavior.
- `repair_attempt`: targeted repair when available locally.
- `checkpoint_create` / `checkpoint_restore`: rollback around risky edits.
- `runtime_memory`: recover refs, artifacts, observations, failures without dumping full history.

## Local Diagnostics Commands

Run only when repo-level proof is needed beyond normal MCP verification:

```powershell
python -m src.diagnostics check
python -m src.diagnostics diagnose
python -m src.diagnostics create
python -m pytest tests -q
python -m pytest tests/integration -m integration -v
```

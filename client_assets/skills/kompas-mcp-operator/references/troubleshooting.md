# Troubleshooting

Primary diagnosis flow now lives in `../SKILL.md`.

Use this file only for extra local commands:

```bash
python -m src.diagnostics check
python -m src.diagnostics diagnose
python -m src.diagnostics create
python -m pytest tests/unit -v
python -m pytest tests/integration -m integration -v
```

Run these only when repo-level proof is needed beyond normal MCP verification.

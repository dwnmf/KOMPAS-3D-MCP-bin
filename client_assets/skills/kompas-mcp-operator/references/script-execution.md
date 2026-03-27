# Script Execution

The main script-selection algorithm now lives in `../SKILL.md`.

Use this file only for quick script reminders:

- Prefer `call_tool(...)` or `tools.<name>(...)` over raw COM when an MCP tool exists.
- Keep a small success guard around tool results.
- Save outputs to explicit paths.
- Return compact summary data.

Useful injected objects:
- `tools`
- `toolbox`
- `call_tool`
- `mcp`
- `sketch`
- `grid`

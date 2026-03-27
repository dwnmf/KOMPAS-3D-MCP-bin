# Runtime Nuances

Most runtime rules now live in `../SKILL.md`.

Keep these repo-specific reminders:

- Prefer `document_path` after the first save.
- `set_3d_view` preset names are strict.
- `clean_view=true` reduces clutter but does not guarantee overlay-free screenshots.
- A visible model can already exist while the caller still waits on response serialization.

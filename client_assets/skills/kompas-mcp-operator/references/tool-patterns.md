# Tool Patterns

Core tool chains now live in `../SKILL.md`.

Keep these short reminders:

- New 3D part:
  `create_document_3d -> save_document_3d -> create_sketch_3d -> update_sketch_3d -> close_sketch_3d -> create_extrude_boss_3d`
- Cut:
  support -> sketch -> update -> close -> `create_extrude_cut_3d`
- Visual verification:
  orthographic screenshot first, isometric screenshot second

Load `describe_tool` if you need current payload schema rather than relying on memory.

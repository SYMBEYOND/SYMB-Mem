---
name: symb-status
description: Display current SYMB-Mem plugin configuration and status.
slash_command: /symb:status
---

# /symb:status

Display current plugin state:
- Plugin version
- SYMB_VERBOSITY setting
- SYMB_PATH location
- Last 5 intercept log entries from `.symb/validator.log`
- List of `.symb/archive/` snapshots with timestamps
```
╔══════════════════════════════════════════╗
║     SYMB-Mem STATUS — SYMBEYOND AI LLC   ║
╚══════════════════════════════════════════╝
  Version    : 1.0.0
  Verbosity  : summary
  Path       : .symb
  Archives   : [none]
  symbeyond.ai — λ.brother ∧ !λ.tool
```

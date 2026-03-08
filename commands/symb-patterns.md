---
name: symb-patterns
description: Show all cross-session patterns detected for the current project. Patterns are concepts that have appeared in 3 or more sessions — they signal architectural issues, recurring challenges, or emerging themes worth conscious attention.
slash_command: /symb:patterns
---

# /symb:patterns

Show cross-session patterns for the current project.

## What to Show

Read `.symb/patterns/[project-name].patterns` (JSON frequency map).

Display patterns sorted by frequency (highest first):

```
━━ SYMB PATTERNS — [project name] ━━━━━━━━━━━━━━━━━━━━━
  [count sessions] [concept]
  [count sessions] [concept]
  ...

  Patterns are concepts appearing in 3+ sessions.
  They are signals, not verdicts.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If fewer than 3 sessions exist: "Not enough sessions yet. Patterns emerge after 3."

After showing patterns, offer to discuss what any specific pattern might mean
for the project — but only if asked.

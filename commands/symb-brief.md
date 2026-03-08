---
name: symb-brief
description: Display the SYMB briefing for the current project. Shows last session summary, active patterns, and next direction.
slash_command: /symb:brief
---

# /symb:brief

Read `.symb/sessions/` for the most recent session file.

Output:
```
━━ SYMB BRIEFING — [project] ━━━━━━━━━━━━━━━━━━━━━━
Last session : [date] ([duration])
Resolved     : [what was solved]
Watch for    : [active pattern or known risk]
Next         : [where to pick up]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If no sessions exist: "No previous sessions. This is the beginning."

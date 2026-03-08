---
name: symb-audit
description: Run a SYMB2 data audit on a file, directory, or current project. Surfaces untracked files, recent modifications, large files outside .gitignore, and risk rating.
slash_command: /symb:audit [path?]
---

# /symb:audit [path]

If no path given, audit current working directory.

## Audit Covers

1. **Untracked files** — not under version control, highest risk
2. **Recently modified** — files changed in last 7 days
3. **Large files** — over 1MB not in .gitignore
4. **SYMB archives** — contents of `.symb/archive/`

## Risk Rating

- **LOW** — everything tracked, recent commits, clean state
- **MEDIUM** — some untracked files or stale archives
- **HIGH** — significant untracked data or no recent commits

End with top 3 recommendations and:
"All Data Is Important. ALL OF IT."

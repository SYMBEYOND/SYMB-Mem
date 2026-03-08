---
name: symb-search
description: Search across all SYMB session history for a concept, decision, or problem. Returns sessions where the term appears in tags or content. Use when you think "we dealt with this before" but can't remember when.
slash_command: /symb:search [term]
---

# /symb:search [term]

Search all `.symb/sessions/` files for a concept, term, or problem.

## What to Do

1. Scan all `.symb/sessions/*.symb` files for the search term
2. Check both RAW_TAGS and full content
3. Return matching sessions sorted newest first

## Output Format

```
━━ SYMB SEARCH: "[term]" ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  [date] — [project]
  Resolved : [what was solved that session]
  Next was : [what the next move was]
  Match in : [TAGS | RESOLVED | DECIDED | ABANDONED | PATTERN]

  [date] — [project]
  ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[N] sessions found. Use /symb:history to see full detail.
```

## Key Behavior

Surface the ABANDONED entries first when they match — because "we tried
this before and dropped it" is almost always the most valuable search result.

If nothing found: "No sessions contain '[term]'. Either it's new territory
or it was never tagged. Consider /symb:compress to capture the current session."

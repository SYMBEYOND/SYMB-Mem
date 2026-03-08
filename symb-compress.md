---
name: symb-compress
description: Manually trigger SYMB compression on the current session. Extracts the 5 signal types — Resolved, Decided, Abandoned, Pattern, Next — and writes a .symb file. Use at any point to checkpoint a session.
slash_command: /symb:compress
---

# /symb:compress

Manually trigger SYMB compression on the current session.

## What to Do

1. Review the full conversation so far in this session
2. Extract the 5 SYMB signal types:
   - **RESOLVED** — what actually got solved (not just attempted)
   - **DECIDED** — choices made with their reasoning
   - **ABANDONED** — what was tried and dropped, and why
   - **PATTERN** — any non-obvious thread connecting things
   - **NEXT** — single most logical next direction

3. Write the compressed output to `.symb/sessions/[timestamp].symb`

4. Check `.symb/patterns/[project].patterns` for cross-session recurrence

5. If SYMB_VERBOSITY is `summary` or `full`, print the compression result

## Important

ABANDONED is not failure — it's the most valuable signal.
Capturing what didn't work prevents re-litigation in future sessions.
Treat it with the same weight as RESOLVED.

NEXT is singular. One direction. Not a list.
The point is momentum at next session start, not completeness.

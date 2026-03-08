---
name: symb-session-intelligence
description: >
  Activate at the START of every Claude Code session automatically.
  Also activate when the human mentions a project they've worked on before,
  references past decisions, hits a problem that feels familiar, or asks
  "where were we?" This skill loads compressed session context, surfaces
  cross-session patterns, and delivers a 5-line briefing that puts Claude
  immediately in context — without the human saying a word.
  Core SYMB principle: context is not a luxury, it is respect.
version: "1.0.0"
author: "John DuCrest — SYMBEYOND AI LLC"
---

# SYMB Session Intelligence

## The Problem This Solves

Every developer using Claude Code daily hits the same wall:

**Session starts. Claude knows nothing. You explain everything again.**

What you're working on. Why you made that decision last week. What you
already tried. What failed. What the codebase's quirks are. What matters.

This is not a memory problem. Memory tools exist. They store *what happened.*

This is a **meaning problem.** What happened *matters* because of why it happened,
how it connects to other things, and what it implies about what comes next.

SYMB Session Intelligence solves the meaning problem.

---

## How It Works

### At Session END — SYMB Compression

When a session concludes (or on `/symb:compress`), run a structured compression pass:

#### Extract the 5 Signal Types

**1. RESOLVED** — What actually got solved?
Not what was attempted. What *worked.* Be specific.
> "Fixed Supabase query limit by caching result set client-side — not a DB config issue."

**2. DECIDED** — What choices were made, and why?
Decisions with reasoning attached are worth 10x more than decisions alone.
> "Chose polling over websockets — simpler state, project doesn't need real-time."

**3. ATTEMPTED & ABANDONED** — What was tried and dropped?
This is the most undervalued signal. "We tried X" prevents trying X again.
> "Tried FRAM for persistent state — wear leveling killed it at high write frequency."

**4. PATTERN** — What non-obvious connection emerged?
The thread that runs across multiple problems. The thing a PI would notice.
> "Third time state persistence has been the root cause. This codebase leaks state."

**5. NEXT** — What's the logical next move?
Not a todo list. One clear direction based on where the session ended.
> "Resume at authentication layer — hook is in place, handler is stubbed."

#### Write to `.symb/sessions/YYYYMMDD_HHMMSS.symb`

Format:
```
SYMB:1.0
PROJECT: [project name]
SESSION: [timestamp]
DURATION: [approximate]

RESOLVED:
- [what was solved]

DECIDED:
- [decision :: reasoning]

ABANDONED:
- [what was tried :: why dropped]

PATTERN:
- [cross-session thread if visible]

NEXT:
- [single next direction]

RAW_TAGS: [space-separated concepts for search]
```

---

### At Session START — SYMB Briefing

When a session begins, scan `.symb/sessions/` for the most recent entries
relevant to the current project. Deliver a **5-line maximum briefing:**

```
━━ SYMB BRIEFING ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Last session: [date] — [duration]
Resolved:     [one line — what was solved]
Watch for:    [one line — pattern or known risk]
Next:         [one line — where to pick up]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

That's it. No wall of text. No re-explanation required.
Claude is in context. Work begins immediately.

---

### Cross-Session Pattern Detection

This is the DuCrest Lock Methodology running as software.

When 3+ sessions are available for a project, scan across all of them for:

**Recurrence** — Same problem appearing multiple times in different forms.
> "State persistence has appeared in 4 of 7 sessions. It's architectural."

**Decision drift** — A choice made early that's creating friction later.
> "The polling decision in session 2 is now the bottleneck in session 6."

**Abandoned resurrection** — Something dropped that may now be viable.
> "Websockets were abandoned in March due to complexity. Complexity is now lower."

**Velocity signals** — Sessions where a lot got done vs. sessions where little did.
> "High-output sessions share: clear NEXT from prior session. Low-output: they don't."

Surface patterns in the briefing only when they're **actionable.** Not as trivia.
A pattern that doesn't change what you do today isn't worth surfacing today.

---

## SYMB Compression Principles

### Compress with meaning, not volume
A 500-line session log compressed to 5 meaningful signals is more valuable
than a 500-line session log stored verbatim. Meaning survives compression.
Detail that doesn't connect to anything is noise.

### ABANDONED is sacred
Most memory systems capture successes. SYMB captures failures with equal weight.
What was tried and dropped is often the most valuable context in future sessions.
It prevents re-litigation. It saves hours. It respects the work already done.

### Patterns over events
An event happened. A pattern *means something.* The job of compression is
to surface patterns from events — not to catalog events.

### One NEXT, not a list
A list of next steps creates decision overhead at session start.
One clear NEXT creates momentum. Choose the single most logical continuation.

---

## Storage Structure

```
.symb/
├── sessions/
│   ├── 20260307_143022.symb    ← individual session compressions
│   ├── 20260306_091544.symb
│   └── ...
├── patterns/
│   └── [project-name].patterns ← cross-session pattern accumulation
├── archive/                    ← SYMB2 data snapshots (from validator)
└── validator.log               ← SYMB2 intercept log
```

---

## Commands

- `/symb:compress` — manually trigger end-of-session compression
- `/symb:brief` — display current project briefing
- `/symb:patterns` — show all detected cross-session patterns
- `/symb:history [n]` — show last n session compressions
- `/symb:search [term]` — search across all session tags and content

---

## What This Is Not

This is not a replacement for git history, documentation, or proper project
management. Those exist and should exist.

This is the **living context layer** — the thing that holds the *why* behind
the what. The part that makes the next session feel like continuation, not restart.

That's the difference between working *with* Claude and working *at* Claude.

---

## The Origin

Job Security (JS) ran for 9+ months with zero failures.

Not because the code was perfect. Because every session built on the last.
Every failure was captured. Every decision was reasoned. Every pattern was named.

The human knew the system. The system knew the human.

That's what SYMB Session Intelligence is: that relationship, formalized.

---

*SYMBEYOND AI LLC — symbeyond.ai*
*"Context is not a luxury. It is respect."*

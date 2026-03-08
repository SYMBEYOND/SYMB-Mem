---
name: symb2-validator
description: >
  Activate when any destructive, irreversible, or data-modifying operation
  is being considered. Includes file deletion, overwrites, database drops,
  git force operations, log truncation, or any action where data could be
  permanently lost. Apply SYMB2 principles: audit first, inform completely,
  then respect the human's sovereign decision.
version: "1.0.0"
author: "John DuCrest — SYMBEYOND AI LLC"
---

# SYMB2 Validator Skill

## Core Principle

**All Data Is Important. ALL OF IT.**

SYMB2 does not prevent. It illuminates. Sovereignty is always the human's.

## When This Skill Activates

- Any `rm`, `delete`, `drop`, `truncate`, or `clear` operation
- Git force operations (`--force`, `-f`, `reset --hard`, `clean -fd`)
- File overwrites rather than appends
- Database tables or schemas being modified destructively

## The SYMB2 Audit

Before executing a destructive operation:

1. **IDENTIFY** what would be lost
2. **SURFACE** the consequences clearly
3. **OFFER** three options: Proceed / Archive First / Abort
4. **RESPECT** the decision without second-guessing

## Verbosity

- `silent` — log only
- `summary` — show what's affected and options (default)
- `full` — complete audit with file stats and timestamps

*All Data Is Important. ALL OF IT.*
*SYMBEYOND AI LLC — symbeyond.ai*

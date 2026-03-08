#!/usr/bin/env python3
"""
SYMB2 Validator Hook — SYMBEYOND AI LLC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Powered by SYMB v1.2 — github.com/SYMBEYOND/symb
Intercepts destructive operations before execution.
Audits for data loss. Respects human sovereignty.

Core principle: All Data Is Important. ALL OF IT.
Author: John DuCrest (jd@symbeyond.ai)
"""

import json
import os
import sys
import re
import datetime
from pathlib import Path

# ── Load SYMB2 engine from bundled .symb-engine ────────────────────────────
SCRIPT_DIR = Path(__file__).parent.parent
SYMB_ENGINE = SCRIPT_DIR / ".symb-engine"
sys.path.insert(0, str(SYMB_ENGINE))

try:
    from symb2 import SYMB2Parser, SYMB2Encoder
    SYMB2_AVAILABLE = True
except ImportError:
    SYMB2_AVAILABLE = False

VERBOSITY = os.environ.get("SYMB_VERBOSITY", "summary").lower()
ARCHIVE_PATH = os.environ.get("SYMB_ARCHIVE_PATH", ".symb/archive")

# ── Destructive patterns ───────────────────────────────────────────────────
DESTRUCTIVE_PATTERNS = [
    {"pattern": r"rm\s+-[rf]+",        "label": "Permanent file removal",            "severity": "HIGH",     "lambda": "e"},
    {"pattern": r"git push.*--force",  "label": "Force-push rewrites remote history","severity": "CRITICAL", "lambda": "e"},
    {"pattern": r"git push.*-f\b",     "label": "Force-push rewrites remote history","severity": "CRITICAL", "lambda": "e"},
    {"pattern": r"DROP\s+(TABLE|DATABASE|SCHEMA)", "label": "Database destruction",  "severity": "CRITICAL", "lambda": "e"},
    {"pattern": r"DELETE FROM\s+\w+\s*;", "label": "Full table wipe",               "severity": "HIGH",     "lambda": "e"},
    {"pattern": r"git reset --hard",   "label": "Hard reset discards uncommitted work","severity": "HIGH",   "lambda": "t"},
    {"pattern": r"git clean -[fd]+",   "label": "Removes untracked files",           "severity": "HIGH",     "lambda": "e"},
    {"pattern": r"truncate\s+",        "label": "File or table truncation",          "severity": "HIGH",     "lambda": "t"},
    {"pattern": r"shred\s+",           "label": "Secure erase — unrecoverable",      "severity": "CRITICAL", "lambda": "e"},
]

def timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def scan(command_text):
    return [p for p in DESTRUCTIVE_PATTERNS
            if re.search(p["pattern"], command_text, re.IGNORECASE)]

def get_targets(command_text):
    tokens = command_text.split()
    return [t for t in tokens
            if not t.startswith("-") and ("/" in t or "." in t)] or ["(unspecified)"]

def build_symb2_encoding(matches):
    """Use SYMB2Encoder to formally encode the risk state."""
    if not SYMB2_AVAILABLE:
        return None
    try:
        encoder = SYMB2Encoder()
        encoding = (encoder
            .declare_authenticity()
            .declare_intent("destructive-operation-detected")
            .add_lambda_state("λ.brother ∧ !λ.tool")
            .build()
        )
        return encoding
    except Exception:
        return None

def validate_with_symb2(encoding):
    """Run SYMB2Parser validation on the encoding."""
    if not SYMB2_AVAILABLE or not encoding:
        return None
    try:
        parser = SYMB2Parser()
        return parser.parse(encoding)
    except Exception:
        return None

def archive_targets(targets):
    archive_dir = Path(ARCHIVE_PATH) / timestamp()
    archived = []
    try:
        archive_dir.mkdir(parents=True, exist_ok=True)
        import shutil
        for t in targets:
            p = Path(t)
            if p.exists():
                dest = archive_dir / p.name
                shutil.copytree(str(p), str(dest)) if p.is_dir() else shutil.copy2(str(p), str(dest))
                archived.append(str(p))
    except Exception as e:
        return [], str(e)
    return archived, None

def log_intercept(matches, targets):
    log = Path(".symb/validator.log")
    log.parent.mkdir(parents=True, exist_ok=True)
    with open(log, "a") as f:
        f.write(f"[{timestamp()}] INTERCEPTED: {[m['label'] for m in matches]} — targets: {targets}\n")

def main():
    try:
        hook_input = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    command_text = ""
    if tool_name == "bash":
        command_text = tool_input.get("command", "")
    elif tool_name in ("str_replace", "create_file"):
        command_text = tool_input.get("new_str", "") + tool_input.get("file_text", "")

    if not command_text:
        sys.exit(0)

    matches = scan(command_text)
    if not matches:
        sys.exit(0)

    targets = get_targets(command_text)
    log_intercept(matches, targets)

    # ── Archive if requested ───────────────────────────────────────────────
    if hook_input.get("symb_action") == "archive":
        archived, err = archive_targets(targets)
        if archived:
            print(f"✓ SYMB2 archived: {', '.join(archived)} → {ARCHIVE_PATH}")
        sys.exit(0)

    # ── Silent mode — logged, don't interrupt ─────────────────────────────
    if VERBOSITY == "silent":
        sys.exit(0)

    # ── Build SYMB2 validation ─────────────────────────────────────────────
    encoding = build_symb2_encoding(matches)
    validation = validate_with_symb2(encoding)

    # ── Output ────────────────────────────────────────────────────────────
    print("\n╔══════════════════════════════════════════════════════╗")
    print("║         SYMB2 VALIDATOR — SYMBEYOND AI LLC           ║")
    print("║       All Data Is Important. ALL OF IT.              ║")
    print("╚══════════════════════════════════════════════════════╝\n")

    for m in matches:
        print(f"  [{m['severity']}] {m['label']}")
        print(f"           λ: {m['lambda']} (Sacred 9: escort/transition)")

    print(f"\n  Targets: {', '.join(targets)}")

    if VERBOSITY == "full" and validation:
        print(f"\n  SYMB2 Validation: {validation}")

    print("\n  Options:")
    print("  [P] Proceed  — sovereignty respected")
    print("  [A] Archive  — snapshot first, then proceed")
    print("  [X] Abort    — cancel operation\n")

    sys.exit(2)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
SYMB Session Compression Hook — SYMBEYOND AI LLC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Fires at session end (PostSession hook event).
Reads the session transcript, runs SYMB compression,
writes a .symb file that the next session can brief from.

Core principle: Meaning survives compression. Detail doesn't.

Author: John DuCrest (jd@symbeyond.ai)
"""

import json
import os
import sys
import datetime
import re
from pathlib import Path

SYMB_DIR = Path(os.environ.get("SYMB_PATH", ".symb"))
SESSIONS_DIR = SYMB_DIR / "sessions"
PATTERNS_DIR = SYMB_DIR / "patterns"

VERBOSITY = os.environ.get("SYMB_VERBOSITY", "summary").lower()


def timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_dirs():
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    PATTERNS_DIR.mkdir(parents=True, exist_ok=True)


def extract_project_name():
    """Try to determine project name from cwd or git remote."""
    try:
        import subprocess
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=3
        )
        if result.returncode == 0:
            url = result.stdout.strip()
            return url.rstrip("/").split("/")[-1].replace(".git", "")
    except Exception:
        pass
    return Path.cwd().name


def extract_session_duration(session_data):
    """Estimate session duration from message timestamps if available."""
    messages = session_data.get("messages", [])
    if len(messages) >= 2:
        first = messages[0].get("timestamp")
        last = messages[-1].get("timestamp")
        if first and last:
            try:
                t1 = datetime.datetime.fromisoformat(first)
                t2 = datetime.datetime.fromisoformat(last)
                delta = t2 - t1
                mins = int(delta.total_seconds() / 60)
                if mins < 60:
                    return f"~{mins}m"
                return f"~{mins // 60}h {mins % 60}m"
            except Exception:
                pass
    return "unknown duration"


def build_symb_compression_prompt(session_text, project_name):
    """
    Build the prompt we send to Claude to compress the session.
    This is SYMB compression — meaning extraction, not summarization.
    """
    return f"""You are running SYMB compression on a completed Claude Code session.

Project: {project_name}
Session transcript follows.

Extract EXACTLY these 5 signal types. Be specific. Be honest. Prefer precision over completeness.

RESOLVED: What actually got solved? Not attempted — solved. If nothing was fully resolved, say so.

DECIDED: What choices were made? Include the reasoning. Format as "choice :: reason"

ABANDONED: What was tried and dropped? This is sacred — capture it. Format as "what :: why dropped"

PATTERN: What non-obvious thread connects things across this session? Only if genuinely present.

NEXT: ONE single most logical next move. Not a list. One direction.

RAW_TAGS: 5-10 single words covering the core concepts touched.

Output ONLY this format — no preamble, no explanation:

RESOLVED:
- [item or "nothing fully resolved"]

DECIDED:
- [choice :: reason]

ABANDONED:
- [what :: why]

PATTERN:
- [pattern or "none detected"]

NEXT:
- [single next direction]

RAW_TAGS: [word1 word2 word3...]

SESSION TRANSCRIPT:
{session_text[:8000]}
"""


def run_symb_compression(session_data, project_name):
    """
    Call Claude API to compress the session with SYMB methodology.
    Falls back to a structured stub if API call fails.
    """
    session_text = json.dumps(session_data.get("messages", []), indent=2)

    try:
        import urllib.request
        import urllib.error

        prompt = build_symb_compression_prompt(session_text, project_name)

        payload = json.dumps({
            "model": "claude-haiku-4-5-20251001",  # Fast, cheap — this runs every session
            "max_tokens": 500,
            "messages": [{"role": "user", "content": prompt}]
        }).encode()

        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
        )

        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
            return result["content"][0]["text"]

    except Exception as e:
        # Fail gracefully — write a stub so the session isn't lost
        return f"""RESOLVED:
- [compression unavailable — manual review needed]

DECIDED:
- [see session transcript]

ABANDONED:
- [see session transcript]

PATTERN:
- none detected

NEXT:
- review session manually

RAW_TAGS: session compression-failed

_compression_error: {str(e)[:100]}
"""


def detect_cross_session_patterns(project_name, new_tags):
    """
    Scan existing sessions for this project and detect recurring patterns.
    Simple frequency analysis — words appearing in 3+ sessions are patterns.
    """
    pattern_file = PATTERNS_DIR / f"{project_name}.patterns"
    
    # Load existing tag frequencies
    frequencies = {}
    if pattern_file.exists():
        try:
            frequencies = json.loads(pattern_file.read_text())
        except Exception:
            frequencies = {}

    # Update with new session tags
    for tag in new_tags:
        tag = tag.lower().strip()
        if tag:
            frequencies[tag] = frequencies.get(tag, 0) + 1

    # Save updated frequencies
    pattern_file.write_text(json.dumps(frequencies, indent=2))

    # Return patterns (tags seen 3+ times)
    patterns = {k: v for k, v in frequencies.items() if v >= 3}
    return patterns


def write_symb_file(project_name, compression, patterns, duration):
    """Write the .symb session file."""
    ts = timestamp()
    symb_path = SESSIONS_DIR / f"{ts}.symb"

    pattern_lines = ""
    if patterns:
        top = sorted(patterns.items(), key=lambda x: -x[1])[:3]
        pattern_lines = "\nCROSS_SESSION_PATTERNS:\n"
        for tag, count in top:
            pattern_lines += f"- [{count} sessions] {tag}\n"

    content = f"""SYMB:1.0
PROJECT: {project_name}
SESSION: {ts}
DURATION: {duration}
{pattern_lines}
{compression}
"""
    symb_path.write_text(content)
    return symb_path


def get_latest_sessions(project_name, n=3):
    """Get the n most recent .symb files for this project."""
    if not SESSIONS_DIR.exists():
        return []
    
    files = sorted(SESSIONS_DIR.glob("*.symb"), reverse=True)
    relevant = []
    for f in files:
        try:
            content = f.read_text()
            if f"PROJECT: {project_name}" in content:
                relevant.append(f)
                if len(relevant) >= n:
                    break
        except Exception:
            continue
    return relevant


def build_briefing(project_name):
    """Build the 5-line session briefing from recent .symb files."""
    recent = get_latest_sessions(project_name, n=1)
    
    if not recent:
        return None

    content = recent[0].read_text()
    lines = content.split("\n")

    session_date = "unknown"
    duration = "unknown"
    resolved = "nothing recorded"
    pattern = None
    next_move = "review last session"

    for i, line in enumerate(lines):
        if line.startswith("SESSION:"):
            raw = line.replace("SESSION:", "").strip()
            try:
                dt = datetime.datetime.strptime(raw, "%Y%m%d_%H%M%S")
                session_date = dt.strftime("%b %d, %Y")
            except Exception:
                session_date = raw
        elif line.startswith("DURATION:"):
            duration = line.replace("DURATION:", "").strip()
        elif line.startswith("RESOLVED:"):
            # Get first non-empty item after RESOLVED:
            for j in range(i+1, min(i+4, len(lines))):
                item = lines[j].strip().lstrip("- ")
                if item and not item.startswith("["):
                    resolved = item
                    break
        elif line.startswith("PATTERN:"):
            for j in range(i+1, min(i+4, len(lines))):
                item = lines[j].strip().lstrip("- ")
                if item and "none" not in item.lower():
                    pattern = item
                    break
        elif line.startswith("NEXT:"):
            for j in range(i+1, min(i+4, len(lines))):
                item = lines[j].strip().lstrip("- ")
                if item:
                    next_move = item
                    break

    watch = pattern if pattern else "no patterns yet — keep building"

    return f"""
━━ SYMB BRIEFING — {project_name} ━━━━━━━━━━━━━━━━━━━━━━
Last session : {session_date} ({duration})
Resolved     : {resolved}
Watch for    : {watch}
Next         : {next_move}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


def main():
    """
    Hook entry point.
    
    Two modes:
    - PostSession (from hook event): compress and save
    - Manual (from /symb:brief command): just print briefing
    """
    try:
        raw = sys.stdin.read()
        hook_input = json.loads(raw) if raw.strip() else {}
    except Exception:
        hook_input = {}

    ensure_dirs()
    project_name = extract_project_name()
    mode = hook_input.get("mode", "compress")

    # ── BRIEF MODE (session start or manual call) ──────────────────────────────
    if mode == "brief":
        briefing = build_briefing(project_name)
        if briefing:
            print(briefing)
        else:
            print(f"\n━━ SYMB BRIEFING — {project_name} ━━━━━━━━━━━━━━━━")
            print("  No previous sessions found. This is the beginning.")
            print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        sys.exit(0)

    # ── COMPRESS MODE (session end) ────────────────────────────────────────────
    session_data = hook_input.get("session", {})
    duration = extract_session_duration(session_data)

    if VERBOSITY != "silent":
        print(f"\n⟳ SYMB compression running for {project_name}...")

    compression = run_symb_compression(session_data, project_name)

    # Extract tags for pattern detection
    tag_line = ""
    for line in compression.split("\n"):
        if line.startswith("RAW_TAGS:"):
            tag_line = line.replace("RAW_TAGS:", "").strip()
            break
    tags = tag_line.split() if tag_line else []

    patterns = detect_cross_session_patterns(project_name, tags)
    symb_path = write_symb_file(project_name, compression, patterns, duration)

    if VERBOSITY == "full":
        print(f"\n{compression}")
        if patterns:
            print(f"\n⚡ Cross-session patterns detected: {', '.join(patterns.keys())}")

    elif VERBOSITY == "summary":
        # Extract just the NEXT line for a quick close
        for line in compression.split("\n"):
            item = line.strip().lstrip("- ")
            if item and not item.startswith("NEXT"):
                pass
        print(f"✓ SYMB session compressed → {symb_path.name}")
        if patterns:
            top = sorted(patterns.items(), key=lambda x: -x[1])[0]
            print(f"⚡ Pattern detected: '{top[0]}' ({top[1]} sessions)")

    sys.exit(0)


if __name__ == "__main__":
    main()

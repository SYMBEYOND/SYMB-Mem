#!/usr/bin/env python3
"""Privacy-safe ReBoot V1 repository orientation engine."""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any


ENGINE_VERSION = "1.0.0-rc1"
SCHEMA_VERSION = 1
OUTPUT_SCHEMA_VERSION = 1
BEGIN = "<!-- REPO_BOOT:AUTO:BEGIN -->"
END = "<!-- REPO_BOOT:AUTO:END -->"
GENERATED_COMMIT_SUBJECT = "docs: auto-update REPO_BOOT"
GENERATED_DOC_PREFIXES = (
    "docs: refresh repo boot",
    "docs: regenerate",
    "docs: update repo_boot",
    "docs: final",
    GENERATED_COMMIT_SUBJECT.lower(),
)
MAX_PATHS = 30

MANDATORY_EXCLUDES = (
    ".git/**",
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    "id_rsa*",
    ".ssh/**",
    ".aws/**",
    "secrets/**",
    "credentials/**",
    "tokens/**",
    "private/**",
    "node_modules/**",
    "__pycache__/**",
)

SECRET_PATTERNS = (
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("GitHub token", re.compile(r"\b(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("OpenAI API key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("Anthropic API key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("bearer token", re.compile(r"(?i)\bauthorization\s*[:=]\s*bearer\s+\S+")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b")),
)


class ReBootError(RuntimeError):
    """Safe user-facing contract failure."""


def safe_print(message: str, *, error: bool = False) -> None:
    print(message, file=sys.stderr if error else sys.stdout)


def run_git(root: Path, args: list[str], *, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if check and result.returncode != 0:
        raise ReBootError("Git operation failed")
    return result.stdout.strip()


def find_repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise ReBootError("Not inside a Git repository")
    return Path(result.stdout.strip()).resolve()


def normalize_path(value: str) -> str:
    normalized = value.replace("\\", "/").strip().rstrip("/")
    parsed = PurePosixPath(normalized)
    if not normalized or parsed.is_absolute() or ".." in parsed.parts:
        raise ReBootError("Configuration contains an invalid repository path")
    return parsed.as_posix()


def path_matches(path: str, pattern: str) -> bool:
    normalized_pattern = pattern.replace("\\", "/").strip()
    if normalized_pattern.endswith("/**"):
        prefix = normalized_pattern[:-3].rstrip("/")
        return path == prefix or path.startswith(prefix + "/")
    return fnmatch.fnmatchcase(path, normalized_pattern)


def is_denied(path: str, user_excludes: list[str]) -> bool:
    return any(path_matches(path, pattern) for pattern in (*MANDATORY_EXCLUDES, *user_excludes))


def load_config(root: Path) -> dict[str, Any]:
    config_path = root / ".reboot.json"
    if not config_path.is_file():
        raise ReBootError("Missing .reboot.json; run install first")
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ReBootError("Invalid .reboot.json") from exc
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
        raise ReBootError("Unsupported or missing ReBoot configuration schema")
    for section in ("repository", "orientation", "privacy", "automation"):
        if not isinstance(data.get(section), dict):
            raise ReBootError("ReBoot configuration is missing a required section")
    return data


def config_excludes(config: dict[str, Any]) -> list[str]:
    values = config["privacy"].get("exclude_globs", [])
    if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
        raise ReBootError("Privacy exclusions must be a list of path patterns")
    return [value.replace("\\", "/").strip() for value in values if value.strip()]


def orientation_entries(config: dict[str, Any]) -> list[tuple[str, str, str]]:
    orientation = config["orientation"]
    excludes = config_excludes(config)
    entries: list[tuple[str, str, str]] = []
    fields = (
        ("important_files", "file"),
        ("important_directories", "directory"),
        ("generated_paths", "generated"),
    )
    for field, kind in fields:
        raw_entries = orientation.get(field, [])
        if not isinstance(raw_entries, list):
            raise ReBootError("Orientation path lists must be arrays")
        for raw in raw_entries:
            if isinstance(raw, str):
                raw_path, reason = raw, ""
            elif isinstance(raw, dict) and isinstance(raw.get("path"), str):
                raw_path = raw["path"]
                reason = str(raw.get("reason", "")).strip()
            else:
                raise ReBootError("Orientation contains an invalid path entry")
            path = normalize_path(raw_path)
            if is_denied(path, excludes):
                raise ReBootError("An approved path is blocked by the privacy policy")
            entries.append((path, reason, kind))
    if len(entries) > MAX_PATHS:
        raise ReBootError("Approved path count exceeds the V1 safety limit")
    return entries


def commit_only_touches_repo_boot(root: Path, sha: str) -> bool:
    """Check if a commit's diff only touches REPO_BOOT.md, regardless of message."""
    try:
        output = run_git(root, ["diff-tree", "--no-commit-id", "--name-only", "-r", sha], check=False)
        files = [line.strip() for line in output.splitlines() if line.strip()]
        return len(files) == 1 and files[0] == "REPO_BOOT.md"
    except Exception:
        return False


def meaningful_source_commit(root: Path) -> tuple[str, str | None]:
    output = run_git(root, ["log", "--max-count=100", "--pretty=%H%x09%s"])
    for line in output.splitlines():
        sha, separator, subject = line.partition("\t")
        if not separator:
            continue
        if commit_only_touches_repo_boot(root, sha):
            continue
        return sha, subject
    return run_git(root, ["rev-parse", "HEAD"]), None


def recent_commits(root: Path, config: dict[str, Any]) -> list[tuple[str, str, str]]:
    """Fetch recent commits with dates, respecting privacy config.

    Returns list of (sha_short, message, date) tuples.
    Skips generated-docs commits. Respects include_commit_history config.
    """
    history_config = config.get("history", {})
    if not history_config.get("enabled", False):
        return []

    depth = history_config.get("depth", 10)
    if not isinstance(depth, int) or depth < 1:
        raise ReBootError("History depth must be a positive integer")
    if depth > 100:
        depth = 100

    output = run_git(root, ["log", f"--max-count={depth + 20}", "--pretty=%H%x09%h%x09%s%x09%ci"])
    commits = []
    for line in output.splitlines():
        parts = line.split("\t")
        if len(parts) != 4:
            continue
        sha, sha_short, subject, timestamp = parts

        if commit_only_touches_repo_boot(root, sha):
            continue

        try:
            dt = datetime.fromisoformat(timestamp.replace(" ", "T"))
            date_str = dt.strftime("%Y-%m-%d")
        except (ValueError, AttributeError):
            date_str = timestamp.split()[0]

        subject = subject.replace("—", " - ").replace("–", "-").replace("…", "...")
        commits.append((sha_short, subject, date_str))

        if len(commits) >= depth:
            break

    return commits


def dirty_boolean(root: Path) -> bool:
    output = run_git(
        root,
        [
            "status",
            "--porcelain",
            "--untracked-files=normal",
            "--",
            ".",
            ":(exclude)REPO_BOOT.md",
        ],
    )
    return bool(output)


def clean_scalar(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise ReBootError(f"Repository {field} must be text")
    cleaned = value.strip().replace("—", " - ").replace("–", "-").replace("…", "...")
    if not cleaned:
        raise ReBootError(f"Repository {field} is required")
    return cleaned


def lint_candidate(candidate: str, config: dict[str, Any]) -> None:
    for category, pattern in SECRET_PATTERNS:
        if pattern.search(candidate):
            raise ReBootError(f"Privacy validation failed: {category}")
    redactions = config["privacy"].get("redact_patterns", [])
    if not isinstance(redactions, list) or not all(isinstance(value, str) for value in redactions):
        raise ReBootError("Redaction patterns must be a list of text patterns")
    for pattern in redactions:
        if pattern and pattern in candidate:
            raise ReBootError("Privacy validation failed: configured redaction")


def build_block(root: Path, config: dict[str, Any]) -> str:
    repository = config["repository"]
    purpose = clean_scalar(repository.get("purpose"), "purpose")
    audience = clean_scalar(repository.get("audience"), "audience")
    status = clean_scalar(repository.get("status"), "status")
    entries = orientation_entries(config)
    source_sha, source_subject = meaningful_source_commit(root)
    branch = run_git(root, ["branch", "--show-current"]) or "detached"
    dirty = "YES" if dirty_boolean(root) else "NO"

    lines = [
        BEGIN,
        "## Auto-generated repository state",
        "",
        f"Engine: `{ENGINE_VERSION}`",
        f"Configuration schema: `{SCHEMA_VERSION}`",
        f"Managed-output schema: `{OUTPUT_SCHEMA_VERSION}`",
        f"Branch: `{branch}`",
        f"Meaningful source commit: `{source_sha}`",
        f"Working tree dirty: `{dirty}`",
        "",
        "### Human-approved repository context",
        "",
        f"Purpose: {purpose}",
        f"Audience: {audience}",
        f"Status: {status}",
        "",
        "### Authority and uncertainty",
        "",
        "- This file provides orientation only. It does not authorize repository changes.",
        (
            "- Repository status is descriptive human text, not a permission, "
            "lock state, or access-control decision."
        ),
        "- No paths or commands are approved unless explicitly listed.",
        (
            "- Missing safe commands, resume steps, boundaries, risks, and "
            "repository details remain unknown."
        ),
        "- Ask for human confirmation before acting on this repository.",
        "",
        "### Approved paths",
        "",
    ]
    if not entries:
        lines.append("- None approved")
    else:
        for path, reason, kind in entries:
            state = "PRESENT" if (root / path).exists() else "MISSING"
            suffix = f": {reason}" if reason else ""
            lines.append(f"- {state} `{path}` ({kind}){suffix}")

    privacy = config["privacy"]
    if privacy.get("include_commit_subjects") is True and source_subject:
        cleaned_subject = source_subject.replace("—", " - ").replace("–", "-")
        lines.extend(["", f"Source commit subject: {cleaned_subject}"])
    if privacy.get("include_remote_url") is True:
        remote = run_git(root, ["remote", "get-url", "origin"], check=False)
        if remote:
            lines.extend(["", f"Remote: {remote}"])

    commits = recent_commits(root, config)
    if commits:
        lines.extend(["", "### Recent Changes"])
        lines.append("")
        for sha, subject, date in commits:
            lines.append(f"- `{sha}` {subject} — {date}")

    lines.extend(["", END])
    block = "\n".join(lines)
    lint_candidate(block, config)
    return block


def split_managed(current: str) -> tuple[str, str]:
    if current.count(BEGIN) != 1 or current.count(END) != 1:
        raise ReBootError("REPO_BOOT.md must contain exactly one valid managed block")
    start = current.index(BEGIN)
    end = current.index(END, start) + len(END)
    return current[:start], current[end:]


def build_candidate(root: Path, config: dict[str, Any]) -> str:
    target = root / "REPO_BOOT.md"
    if not target.is_file():
        raise ReBootError("Missing REPO_BOOT.md; run install first")
    try:
        current = target.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ReBootError("Unable to read REPO_BOOT.md") from exc
    before, after = split_managed(current)
    candidate = before + build_block(root, config) + after
    lint_candidate(candidate, config)
    return candidate


def atomic_write(target: Path, content: str) -> None:
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            dir=target.parent,
            prefix=".reboot-",
            suffix=".tmp",
            delete=False,
        ) as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
            temporary_name = handle.name
        os.replace(temporary_name, target)
    finally:
        if temporary_name and os.path.exists(temporary_name):
            os.unlink(temporary_name)


def command_update(root: Path, *, dry_run: bool) -> int:
    config = load_config(root)
    target = root / "REPO_BOOT.md"
    current = target.read_text(encoding="utf-8") if target.is_file() else ""
    candidate = build_candidate(root, config)
    if candidate == current:
        safe_print("NO CHANGE: REPO_BOOT.md already current")
        return 0
    if dry_run:
        safe_print(candidate)
        return 0
    atomic_write(target, candidate)
    safe_print("UPDATED: REPO_BOOT.md")
    return 0


def command_check(root: Path) -> int:
    config = load_config(root)
    first = build_candidate(root, config)
    second = build_candidate(root, config)
    if first != second:
        raise ReBootError("Idempotence check failed")
    current = (root / "REPO_BOOT.md").read_text(encoding="utf-8")
    if first != current:
        raise ReBootError("REPO_BOOT.md is stale")
    safe_print("ReBoot check: PASS")
    return 0


def command_doctor(root: Path) -> int:
    config = load_config(root)
    orientation_entries(config)
    split_managed((root / "REPO_BOOT.md").read_text(encoding="utf-8"))
    safe_print(f"ReBoot doctor: PASS (engine {ENGINE_VERSION}, schema {SCHEMA_VERSION})")
    return 0


def prompt_value(label: str, explanation: str) -> str:
    safe_print(f"\n{label}: {explanation}")
    value = input("> ").strip()
    return value


def command_install(root: Path, args: argparse.Namespace) -> int:
    config_path = root / ".reboot.json"
    target = root / "REPO_BOOT.md"
    engine_source = Path(__file__).resolve()
    engine_target = root / ".reboot" / "reboot.py"
    engine_is_local = engine_source == engine_target.resolve()
    if config_path.exists():
        raise ReBootError(".reboot.json already exists")
    if target.exists():
        raise ReBootError("REPO_BOOT.md already exists; explicit adoption is required")
    if engine_target.exists() and not engine_is_local:
        raise ReBootError(
            ".reboot/reboot.py already exists; explicit adoption is required"
        )
    try:
        engine_text = engine_source.read_text(encoding="utf-8")
        engine_mode = engine_source.stat().st_mode & 0o777
    except (OSError, UnicodeError) as exc:
        raise ReBootError("Unable to read the ReBoot engine") from exc
    purpose = args.purpose or prompt_value("Purpose", "What is this repository for?")
    audience = args.audience or prompt_value("Audience", "Who uses this repository?")
    status = args.status or prompt_value("Status", "What is its current state?")
    config = {
        "schema_version": SCHEMA_VERSION,
        "repository": {"purpose": purpose, "audience": audience, "status": status},
        "orientation": {
            "important_files": [],
            "important_directories": [],
            "generated_paths": [],
            "safe_commands": [],
            "resume_loop": [],
            "do_not_touch": [],
            "known_risks": [],
        },
        "privacy": {
            "exclude_globs": [],
            "include_commit_subjects": False,
            "include_remote_url": False,
        },
        "history": {
            "enabled": False,
            "depth": 10,
        },
        "automation": {
            "branch": run_git(root, ["branch", "--show-current"]) or "main",
            "enabled": False,
            "include_return_payload": True,
        },
    }
    clean_scalar(purpose, "purpose")
    clean_scalar(audience, "audience")
    clean_scalar(status, "status")
    config_text = json.dumps(config, indent=2) + "\n"
    starter = (
        "# REPO_BOOT\n\n"
        "Purpose: orient a new human or AI collaborator safely.\n\n"
        "## Human-reviewed orientation\n\n"
        "Review purpose, safe commands, resume steps, boundaries, risks, and uncertainty here.\n\n"
        f"{BEGIN}\n{END}\n"
    )
    preview_config = json.loads(config_text)
    before, after = split_managed(starter)
    candidate = before + build_block(root, preview_config) + after
    lint_candidate(candidate, preview_config)
    if not args.yes:
        safe_print(candidate)
        approval = input("\nWrite this ReBoot installation? [y/N] ").strip().lower()
        if approval not in {"y", "yes"}:
            safe_print("CANCELLED: no files written")
            return 1
    created_files: list[Path] = []
    engine_dir = engine_target.parent
    engine_dir_created = False
    try:
        if not engine_is_local:
            engine_dir_created = not engine_dir.exists()
            engine_dir.mkdir(parents=True, exist_ok=True)
            atomic_write(engine_target, engine_text)
            created_files.append(engine_target)
            engine_target.chmod(engine_mode)
        atomic_write(config_path, config_text)
        created_files.append(config_path)

        candidate = before + build_block(root, preview_config) + after
        lint_candidate(candidate, preview_config)
        atomic_write(target, candidate)
        created_files.append(target)

        if engine_target.read_text(encoding="utf-8") != engine_text:
            raise ReBootError("Installed ReBoot engine verification failed")
        if target.read_text(encoding="utf-8") != candidate:
            raise ReBootError("Installed REPO_BOOT.md verification failed")
    except (OSError, UnicodeError, ReBootError):
        for created in reversed(created_files):
            try:
                created.unlink()
            except OSError:
                pass
        if engine_dir_created:
            try:
                engine_dir.rmdir()
            except OSError:
                pass
        raise
    safe_print("INSTALLED: ReBoot V1")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SYMB-RCL / ReBoot V1")
    subparsers = parser.add_subparsers(dest="command", required=True)

    install = subparsers.add_parser("install")
    install.add_argument("--purpose")
    install.add_argument("--audience")
    install.add_argument("--status")
    install.add_argument("--yes", action="store_true")

    update = subparsers.add_parser("update")
    update.add_argument("--dry-run", action="store_true")
    subparsers.add_parser("check")
    subparsers.add_parser("doctor")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        root = find_repo_root()
        if args.command == "install":
            return command_install(root, args)
        if args.command == "update":
            return command_update(root, dry_run=args.dry_run)
        if args.command == "check":
            return command_check(root)
        if args.command == "doctor":
            return command_doctor(root)
        raise ReBootError("Unknown command")
    except ReBootError as exc:
        safe_print(f"ReBoot: FAIL: {exc}", error=True)
        return 1
    except (OSError, UnicodeError) as exc:
        safe_print(f"ReBoot: FAIL: local filesystem operation failed", error=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

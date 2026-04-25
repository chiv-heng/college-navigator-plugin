#!/usr/bin/env python3
"""PostToolUse hook: warn when a counselor report contains keywords that
typically belong in the private supplement.

Reads the Claude Code PostToolUse JSON payload from stdin. Triggers only
on writes to files matching ``*-counselor-report*``. Keyword list lives
in ``private-keywords.json`` next to this script so it can be tuned and
tested without code changes.

Exit codes follow the Claude Code hook contract:
  0 — no issue (or not applicable)
  2 — warning sent on stderr; Claude sees the message
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HOOK_DIR = Path(__file__).resolve().parent
KEYWORDS_FILE = HOOK_DIR / "private-keywords.json"
COUNSELOR_REPORT_MARKER = "-counselor-report"


def load_keywords(path: Path) -> list[str]:
    """Flatten the categorized keyword config into a single list."""
    data = json.loads(path.read_text())
    keywords: list[str] = []
    for category in data.get("categories", {}).values():
        keywords.extend(category)
    return keywords


def resolve_content(payload: dict) -> str:
    """Return the text we should scan for the given tool invocation.

    Write supplies full ``content``. Edit/MultiEdit only carry the diff,
    so for those we read the file from disk after the operation completes.
    """
    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {})

    if tool_name == "Write":
        return tool_input.get("content", "") or ""

    file_path = tool_input.get("file_path")
    if file_path:
        try:
            return Path(file_path).read_text()
        except (OSError, UnicodeDecodeError):
            return ""
    return ""


def find_matches(content: str, keywords: list[str]) -> list[str]:
    """Return keywords found in content (case-insensitive, deduped, sorted)."""
    haystack = content.lower()
    hits = {kw for kw in keywords if kw.lower() in haystack}
    return sorted(hits)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Malformed payload — don't block; let Claude proceed.
        return 0

    file_path = payload.get("tool_input", {}).get("file_path", "") or ""
    if COUNSELOR_REPORT_MARKER not in file_path:
        return 0

    if not KEYWORDS_FILE.exists():
        print(
            f"WARNING: privacy hook config missing at {KEYWORDS_FILE}. "
            "Privacy guard skipped.",
            file=sys.stderr,
        )
        return 0

    keywords = load_keywords(KEYWORDS_FILE)
    content = resolve_content(payload)
    if not content:
        return 0

    matches = find_matches(content, keywords)
    if not matches:
        return 0

    matched_list = ", ".join(matches)
    print(
        f"WARNING: The counselor report contains keywords that are typically "
        f"private-only: {matched_list}. Verify the student opted to share this "
        f"information, or move these details to the private supplement.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())

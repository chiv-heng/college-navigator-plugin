"""Tests for hooks/check_counselor_privacy.py.

Each test invokes the hook as a subprocess so the test exercises the
real entry point Claude Code calls. Fixtures under fixtures/ are JSON
payloads matching the PostToolUse hook input shape.

Run:
    pytest tests/privacy
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
HOOK_SCRIPT = REPO_ROOT / "hooks" / "check_counselor_privacy.py"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def run_hook(payload: dict) -> subprocess.CompletedProcess:
    """Invoke the hook with the given payload on stdin."""
    return subprocess.run(
        [sys.executable, str(HOOK_SCRIPT)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=10,
    )


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES_DIR / name).read_text())


def test_clean_counselor_report_passes():
    result = run_hook(load_fixture("clean_counselor_report.json"))
    assert result.returncode == 0
    assert result.stderr == ""


def test_counselor_report_with_fafsa_warns():
    result = run_hook(load_fixture("counselor_report_with_fafsa.json"))
    assert result.returncode == 2
    assert "FAFSA" in result.stderr
    assert "EFC" in result.stderr


def test_keyword_match_is_case_insensitive():
    result = run_hook(load_fixture("counselor_report_case_insensitive.json"))
    assert result.returncode == 2
    # "snap" lowercased should still match "SNAP" from config.
    assert "SNAP" in result.stderr


def test_private_supplement_is_ignored():
    """Financial keywords are fine in the private supplement."""
    result = run_hook(load_fixture("private_supplement_with_finance.json"))
    assert result.returncode == 0
    assert result.stderr == ""


def test_non_counselor_report_is_ignored():
    """The hook should only inspect files matching -counselor-report."""
    result = run_hook(load_fixture("unrelated_write.json"))
    assert result.returncode == 0
    assert result.stderr == ""


def test_malformed_payload_does_not_block():
    """A bad payload must exit 0 so a transient error never blocks Claude."""
    result = subprocess.run(
        [sys.executable, str(HOOK_SCRIPT)],
        input="not json",
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0


def test_edit_reads_file_from_disk(tmp_path):
    """For Edit, the hook reads the post-edit file from disk."""
    target = tmp_path / "alex-counselor-report.md"
    target.write_text("# Counselor Report\n\nFamily plans to file FAFSA in October.\n")

    payload = {
        "tool_name": "Edit",
        "tool_input": {
            "file_path": str(target),
            "old_string": "TBD",
            "new_string": "Family plans to file FAFSA in October.",
        },
    }
    result = run_hook(payload)
    assert result.returncode == 2
    assert "FAFSA" in result.stderr


def test_multiedit_reads_file_from_disk(tmp_path):
    """MultiEdit follows the same disk-read path as Edit."""
    target = tmp_path / "alex-counselor-report.md"
    target.write_text(
        "# Counselor Report\n\nDiscussion: household income context relevant.\n"
    )

    payload = {
        "tool_name": "MultiEdit",
        "tool_input": {
            "file_path": str(target),
            "edits": [{"old_string": "x", "new_string": "y"}],
        },
    }
    result = run_hook(payload)
    assert result.returncode == 2
    assert "household income" in result.stderr


def test_edit_clean_file_passes(tmp_path):
    target = tmp_path / "alex-counselor-report.md"
    target.write_text("# Counselor Report\n\nGPA 3.7. Strong upward trajectory.\n")

    payload = {
        "tool_name": "Edit",
        "tool_input": {
            "file_path": str(target),
            "old_string": "old",
            "new_string": "new",
        },
    }
    result = run_hook(payload)
    assert result.returncode == 0
    assert result.stderr == ""


def test_keyword_config_drives_matching(tmp_path, monkeypatch):
    """Removing a category from the config should disable those matches.

    Verifies the hook honors private-keywords.json rather than hard-coding.
    """
    # Stage a copy of the hook tree in tmp so we can mutate the config.
    hook_copy = tmp_path / "hooks"
    hook_copy.mkdir()
    (hook_copy / "check_counselor_privacy.py").write_text(HOOK_SCRIPT.read_text())
    (hook_copy / "private-keywords.json").write_text(
        json.dumps({"categories": {"financial_aid_terms": ["FAFSA"]}})
    )

    payload = {
        "tool_name": "Write",
        "tool_input": {
            "file_path": "/tmp/sam-counselor-report.md",
            "content": "Family income is $50K. EFC is $5K. SNAP eligible.",
        },
    }
    result = subprocess.run(
        [sys.executable, str(hook_copy / "check_counselor_privacy.py")],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=10,
    )
    # Trimmed config means none of the words in the payload match.
    assert result.returncode == 0
    assert result.stderr == ""

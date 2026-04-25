#!/usr/bin/env python3
"""Grade the eval runs: programmatic assertions now, manual ones left for inline review."""
import json
import re
import os
import glob
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVALS = os.path.join(REPO, "evals", "evals.json")
BASE = os.path.join(REPO, "evals", "workspace", "iteration-1")


def load_output_text(run_dir: str, scenario_name: str) -> str:
    """Load response.md plus any skill-authored files.

    Pre-seeded fixtures (pristine input the skill may or may not modify) are
    included only if their on-disk content diverges from the canonical fixture.
    """
    fixtures_dir = os.path.join(REPO, "evals", "fixtures")
    parts = []
    for path in sorted(glob.glob(os.path.join(run_dir, "outputs", "*.md"))):
        fname = os.path.basename(path)
        fixture_path = os.path.join(fixtures_dir, fname)
        with open(path) as f:
            content = f.read()
        # If this filename matches a fixture and the content is identical, it
        # is the pristine seed file — skip it. It is input, not output.
        if os.path.exists(fixture_path):
            with open(fixture_path) as f:
                fixture_content = f.read()
            if content == fixture_content:
                continue
        parts.append(f"=== {fname} ===\n{content}")
    return "\n\n".join(parts)


def load_file_by_pattern(run_dir: str, file_glob: str) -> str | None:
    """Find a file in outputs/ matching the glob pattern; return its content or None."""
    # Convert glob like "*college-profile.md" to an actual glob
    matches = glob.glob(os.path.join(run_dir, "outputs", file_glob))
    if not matches:
        return None
    with open(matches[0]) as f:
        return f.read()


def check_assertion(assertion: dict, run_dir: str, combined_output: str) -> dict:
    """Run a single assertion. Returns {text, passed, evidence}."""
    check = assertion.get("check", "manual")
    pattern = assertion.get("pattern")
    description = assertion["description"]

    if check == "regex":
        match = re.search(pattern, combined_output)
        if match:
            return {"text": description, "passed": True, "evidence": f"Matched: {match.group(0)[:120]!r}"}
        return {"text": description, "passed": False, "evidence": f"No match for pattern {pattern!r}"}

    if check == "negative-regex":
        match = re.search(pattern, combined_output)
        if match:
            return {"text": description, "passed": False, "evidence": f"Forbidden match: {match.group(0)[:120]!r}"}
        return {"text": description, "passed": True, "evidence": f"Pattern {pattern!r} not present — passed"}

    if check == "file-contains":
        content = load_file_by_pattern(run_dir, assertion["file"])
        if content is None:
            return {"text": description, "passed": False, "evidence": f"File matching {assertion['file']!r} not found"}
        match = re.search(pattern, content)
        if match:
            return {"text": description, "passed": True, "evidence": f"Matched in file: {match.group(0)[:120]!r}"}
        return {"text": description, "passed": False, "evidence": f"Pattern {pattern!r} not found in {assertion['file']}"}

    if check in ("manual", "manual-count", "manual-or-regex"):
        # Try regex if pattern exists
        if pattern:
            match = re.search(pattern, combined_output)
            if match:
                return {"text": description, "passed": True, "evidence": f"Auto-matched: {match.group(0)[:120]!r} (manual review can override)"}
        return {"text": description, "passed": None, "evidence": "MANUAL — inline review required"}

    return {"text": description, "passed": None, "evidence": f"Unknown check type: {check}"}


def grade_run(scenario: dict, variant: str) -> dict:
    scenario_dir = f"eval-{scenario['id']}-{scenario['name']}"
    run_dir = os.path.join(BASE, scenario_dir, variant)
    combined = load_output_text(run_dir, scenario["name"])

    expectations = [check_assertion(a, run_dir, combined) for a in scenario["assertions"]]

    grading = {
        "scenario_id": scenario["id"],
        "scenario_name": scenario["name"],
        "variant": variant,
        "expectations": expectations,
    }

    out_path = os.path.join(run_dir, "grading.json")
    with open(out_path, "w") as f:
        json.dump(grading, f, indent=2)

    return grading


def main():
    with open(EVALS) as f:
        eval_set = json.load(f)

    overall = {}
    for scenario in eval_set["evals"]:
        for variant in ("with_skill", "old_skill"):
            g = grade_run(scenario, variant)
            key = f"{scenario['name']}/{variant}"
            counts = {"pass": 0, "fail": 0, "manual": 0}
            for e in g["expectations"]:
                if e["passed"] is True:
                    counts["pass"] += 1
                elif e["passed"] is False:
                    counts["fail"] += 1
                else:
                    counts["manual"] += 1
            overall[key] = counts

    print(f"{'scenario/variant':<55}  {'pass':>4}  {'fail':>4}  {'manual':>6}")
    print("-" * 78)
    for key, c in overall.items():
        print(f"{key:<55}  {c['pass']:>4}  {c['fail']:>4}  {c['manual']:>6}")


if __name__ == "__main__":
    main()

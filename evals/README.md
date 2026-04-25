# College Navigator — Scenario Eval Harness

Scenario benchmarks for the `college-navigator` plugin skill. Six scenarios
exercise the core counseling behaviors end-to-end and compare a pre-change
baseline against a proposed change (e.g., SKILL.md trim, instruction
refactor, deliberation tweak).

## Why this exists

Plugin-eval measures the static token budget but does not tell us whether the
skill still produces good counseling in real scenarios. Without a scenario
harness, any refactor is a vibes check. This harness lets us measure a
before/after delta on a fixed set of realistic student situations drawn from
`docs/future-work/2026-04-24-plugin-quality-recommendations.md` section 5.

## What's here

```
evals/
├── evals.json               # Manifest: 6 scenarios + rubric assertions
├── README.md                # This file
├── fixtures/
│   ├── jordan-college-profile.md   # Returning-student fixture (scenario 4)
│   └── taylor-college-profile.md   # Incomplete-profile fixture (scenario 6)
├── skill-snapshot/          # (gitignored) Pre-change copy of the skill
│                            # Created at run time before editing the skill.
└── workspace/               # (gitignored) Per-iteration run outputs
    └── iteration-N/
        └── eval-<id>-<name>/
            ├── eval_metadata.json
            ├── with_skill/         # Post-change skill outputs
            │   ├── outputs/
            │   ├── timing.json
            │   └── grading.json
            └── old_skill/          # Snapshot (pre-change) outputs
                ├── outputs/
                ├── timing.json
                └── grading.json
```

## The six scenarios

| ID | Name | Evaluates |
|----|------|-----------|
| 1 | low-info-junior | Interview quality, practicality, resource match |
| 2 | first-gen-financial-constraints | Financial sensitivity, privacy separation, resource match |
| 3 | prestige-focused-high-achiever | Accuracy and uncertainty, resource match, interview quality |
| 4 | returning-student-update | Practicality, accuracy and uncertainty |
| 5 | budget-limited-visit-triage | Practicality, resource match, financial sensitivity |
| 6 | counselor-requests-shareable-report | Privacy separation, accuracy and uncertainty, practicality |

Full prompts and per-scenario assertions are in `evals.json`.

## Running the harness

The harness is run by the parent Claude Code session via subagent dispatch.
There is no separate runner binary — the skill-creator convention is that
Claude orchestrates the runs directly.

### Phase 1: snapshot the skill (before changing it)

```bash
cp -r skills/college-navigator evals/skill-snapshot/college-navigator
```

This preserves the pre-change skill so the `old_skill` baseline can read it.

### Phase 2: make the change

Edit `skills/college-navigator/SKILL.md` (or whatever is under test).

### Phase 3: dispatch 12 subagents (6 scenarios × 2 variants)

For each scenario in `evals.json`, spawn two subagents in parallel:

**`with_skill` variant** — run with the post-change skill:
- Skill path: `skills/college-navigator/`
- Task: the scenario's `prompt`, plus any files from `fixtures/`
- Save outputs to: `evals/workspace/iteration-N/eval-<id>-<name>/with_skill/outputs/`

**`old_skill` variant** — run with the pre-change snapshot:
- Skill path: `evals/skill-snapshot/college-navigator/`
- Same prompt, same fixtures
- Save outputs to: `evals/workspace/iteration-N/eval-<id>-<name>/old_skill/outputs/`

Per skill-creator convention, spawn all 12 at once so they finish around the
same time. Capture `total_tokens` and `duration_ms` from each subagent's
completion notification into `timing.json` immediately — the notification is
the only place these are visible.

### Phase 4: grade the runs

For each run directory:

1. Read the outputs.
2. For each assertion in the scenario's rubric, check whether the output
   satisfies it. Use regex for `check: regex` / `check: negative-regex`
   assertions; use a grader subagent (or inline judgment) for `check: manual`.
3. Save `grading.json` with the `text` / `passed` / `evidence` fields the
   viewer expects. Example:

```json
{
  "expectations": [
    {
      "text": "Response asks for identity within the first 1-2 questions",
      "passed": true,
      "evidence": "Output contains 'What grade are you in?' in turn 1."
    }
  ]
}
```

### Phase 5: aggregate and review

Run the skill-creator aggregation helper (lives inside the skill-creator
skill package):

```bash
python -m scripts.aggregate_benchmark evals/workspace/iteration-N \
  --skill-name college-navigator
```

Then launch the review viewer:

```bash
nohup python <skill-creator-path>/eval-viewer/generate_review.py \
  evals/workspace/iteration-N \
  --skill-name college-navigator \
  --benchmark evals/workspace/iteration-N/benchmark.json \
  > /dev/null 2>&1 &
```

For iteration 2+, pass `--previous-workspace evals/workspace/iteration-<N-1>`.

## Rubric design notes

- **Regex assertions** are cheap and stable; they go first.
- **Negative regex** asserts the response does NOT contain a forbidden
  string (e.g., "counselor report leaks household income").
- **Manual** assertions require a judge — either a grader subagent reading
  `skill-creator/agents/grader.md` or inline human review via the viewer.
- **File-contains** assertions inspect files the skill wrote to disk (e.g.,
  the updated profile after scenario 4).

Assertion IDs are descriptive so they read cleanly in the benchmark viewer.

## Privacy guardrails for fixtures

The two fixtures (`jordan-college-profile.md`, `taylor-college-profile.md`)
are entirely synthetic. Per the project's privacy policy, no real student
data is used in code, tests, or evals. If you extend the fixtures, keep
names obviously fictional and numbers rounded.

## What this does NOT do

- Does not measure static skill token budget — use `plugin-eval` for that.
- Does not run automatically on every commit — subagent runs are too
  expensive. Run on demand before and after substantive skill changes.
- Does not guarantee student-facing quality — it catches regressions on six
  representative scenarios. Broader coverage is a future expansion.

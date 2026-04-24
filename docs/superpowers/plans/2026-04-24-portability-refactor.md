# College Navigator Portability Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Separate the portable counseling model from Claude-specific runtime behavior so ChatGPT, Gemini, Codex, and future adapters can share one canonical core.

**Architecture:** Keep Claude Code and Claude Desktop as the full reference runtime. Add a model-agnostic core under `platforms/model-agnostic/`, then make each platform adapter explicitly derive from that core and document which runtime capabilities it adds or loses. Do not remove existing Claude commands, agents, hooks, or report generation.

**Tech Stack:** Markdown instruction packages, Claude plugin manifest, shell privacy hook, Python PDF generator, optional Node-based static validation scripts.

---

## File Structure

- Create `platforms/model-agnostic/README.md`
  - Explains the portable kernel, adapter contract, and what must remain runtime-specific.
- Create `platforms/model-agnostic/core-instructions.md`
  - Canonical portable counseling instructions with no Claude tool names, slash commands, hooks, or local filesystem assumptions.
- Create `platforms/model-agnostic/runtime-capability-matrix.md`
  - Defines capability tiers: core counseling parity, workflow parity, and safety parity.
- Create `platforms/model-agnostic/adapter-contract.md`
  - Checklist every platform adapter must satisfy.
- Create `scripts/check-portability.sh`
  - Static guard that fails when model-agnostic files contain Claude runtime terms.
- Create `tests/portability/README.md`
  - Human-readable test cases for expected behavior across platforms.
- Modify `platforms/README.md`
  - Point to the model-agnostic core as the shared source for platform packages.
- Modify `platforms/custom-gpt/PARITY.md`
  - Reframe parity around the three tiers.
- Modify `platforms/custom-gpt/instructions.md`
  - Add a brief provenance note that this file derives from the model-agnostic core.
- Modify `platforms/gemini-gem/README.md`
  - Link to the capability matrix and instruction-priority rules.
- Modify `platforms/gemini-gem/instructions.md`
  - Add the same provenance note.
- Modify `platforms/SYNC_LOG.md`
  - Track the new model-agnostic files and adapter sync dates.
- Do not modify `skills/college-navigator/SKILL.md` in this first pass unless a sync note needs a wording correction.
- Do not modify `.claude-plugin/plugin.json`, `commands/college-navigator.md`, `agents/*.md`, or `hooks/*` in this first pass.

## Task 1: Add The Model-Agnostic Package

**Files:**
- Create: `platforms/model-agnostic/README.md`
- Create: `platforms/model-agnostic/core-instructions.md`
- Create: `platforms/model-agnostic/runtime-capability-matrix.md`
- Create: `platforms/model-agnostic/adapter-contract.md`

- [ ] **Step 1: Create the model-agnostic README**

Write `platforms/model-agnostic/README.md` with this structure:

```markdown
# College Navigator Model-Agnostic Core

This folder contains the portable counseling kernel for College Navigator.
It is the shared source for platform adapters that cannot run the full Claude
plugin runtime.

## What Belongs Here

- Counseling philosophy
- Interview structure
- Financial aid framing
- Resource assessment logic
- Gap analysis lens
- Visit optimization lens
- Report content rules
- Privacy-by-design expectations

## What Does Not Belong Here

- Slash commands
- Claude Code tool names
- Claude Desktop plugin packaging
- PostToolUse hooks
- Local filesystem persistence requirements
- Shell or Python execution instructions
- Claims that a platform has true subagents unless it does

## Adapter Rule

Every platform adapter must state which capabilities are native, simulated,
manual, or unavailable. Use `runtime-capability-matrix.md` as the source of
truth for those claims.
```

- [ ] **Step 2: Create the portable core instructions**

Write `platforms/model-agnostic/core-instructions.md` by extracting the durable counseling behavior from `skills/college-navigator/SKILL.md` and `platforms/custom-gpt/instructions.md`.

The file must include these sections in this order:

```markdown
# College Navigator Core Instructions

## Role
## Who This Serves
## Counseling Philosophy
## Interview Philosophy
## Profile Structure
## Adaptive Interview Flow
## Financial Context Handling
## Resource Assessment
## College List Strategy
## Gap Analysis Lens
## Visit Optimization Lens
## Report Types
## Privacy Rules
## Current Information Rules
## Output Style
```

Use these constraints while writing:

- Do not mention Claude, Claude Code, Claude Desktop, ChatGPT, Gemini, Codex, or any platform name.
- Do not mention slash commands.
- Do not require reading or writing local files.
- Do not mention hooks, shell scripts, `jq`, `bash`, or tool names.
- Phrase persistence as optional: "If the platform supports persistent files or memory..."
- Phrase multi-agent deliberation as portable reasoning: "Before strategic recommendations, reason from three perspectives..."

- [ ] **Step 3: Create the runtime capability matrix**

Write `platforms/model-agnostic/runtime-capability-matrix.md` with this table:

```markdown
# Runtime Capability Matrix

| Capability | Core Counseling Parity | Workflow Parity | Safety Parity | Notes |
|------------|------------------------|-----------------|---------------|-------|
| Adaptive interview | Native | Native | N/A | Conversation-only platforms can do this well. |
| Reference knowledge | Native if files or long instructions are available | Adapter-specific | N/A | Custom GPT can use Knowledge files. Gemini may need compressed instructions. |
| Gap analysis | Native as reasoning lens | Simulated if no subagents | N/A | True separate agents are runtime-specific. |
| Visit optimization | Native as reasoning lens | Simulated if no subagents | N/A | The decision logic ports better than the orchestration. |
| Multi-agent deliberation | Simulated | Native only where agent routing exists | N/A | Never claim true subagents unless the runtime supports them. |
| Session continuity | Manual unless storage exists | Native only with files, memory, or backend | N/A | Paste-in resume is not workflow parity. |
| Report generation | Native as text | Native only with file/export support | Partial | File-first updates require storage. |
| Privacy split | Native as instruction | Partial | Strong only with validation hook or backend check | Prompt-only privacy is not equivalent to automated enforcement. |
| Current school data | Native if browsing/search exists | Adapter-specific | N/A | Require source/date awareness for changing data. |
| Slash command entrypoint | N/A | Native only where commands exist | N/A | Use natural-language starters elsewhere. |
```

- [ ] **Step 4: Create the adapter contract**

Write `platforms/model-agnostic/adapter-contract.md` with this checklist:

```markdown
# Platform Adapter Contract

Every College Navigator platform adapter must document:

- [ ] Setup path for a non-technical counselor, parent, or student
- [ ] Which source files were used
- [ ] Whether the adapter uses uploaded knowledge, pasted instructions, retrieval, or a backend
- [ ] Whether session continuity is native, manual, or unavailable
- [ ] Whether report output is chat-only, downloadable, file-backed, or exported
- [ ] Whether privacy validation is automated or instruction-only
- [ ] Whether gap analysis and visit optimization are true agents or single-model perspectives
- [ ] How current college data should be verified
- [ ] What the user must do to resume a previous student profile
- [ ] What is intentionally out of scope
```

- [ ] **Step 5: Verify no platform-specific terms entered the core**

Run:

```bash
rg -n "Claude|ChatGPT|Gemini|Codex|slash|PostToolUse|CLAUDE|Write|Read|Task|bash|jq|filesystem|local file" platforms/model-agnostic
```

Expected: No matches, except in `README.md` under "What Does Not Belong Here" if that wording is kept.

- [ ] **Step 6: Commit**

```bash
git add platforms/model-agnostic
git commit -m "docs: add model-agnostic college navigator core"
```

## Task 2: Add A Static Portability Guard

**Files:**
- Create: `scripts/check-portability.sh`
- Create: `tests/portability/README.md`

- [ ] **Step 1: Create the portability check script**

Write `scripts/check-portability.sh`:

```bash
#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CORE_FILE="${ROOT_DIR}/platforms/model-agnostic/core-instructions.md"

if [[ ! -f "$CORE_FILE" ]]; then
  echo "Missing model-agnostic core: $CORE_FILE" >&2
  exit 1
fi

blocked_terms=(
  "Claude"
  "Claude Code"
  "Claude Desktop"
  "ChatGPT"
  "Gemini"
  "Codex"
  "PostToolUse"
  "CLAUDE_PLUGIN_ROOT"
  "slash command"
  "/college-navigator"
  "bash"
  "jq"
  "Write tool"
  "Read tool"
  "Task tool"
)

failed=0
for term in "${blocked_terms[@]}"; do
  if grep -nF "$term" "$CORE_FILE" >/tmp/college-navigator-portability-match.txt; then
    echo "Blocked platform-specific term in core-instructions.md: $term" >&2
    cat /tmp/college-navigator-portability-match.txt >&2
    failed=1
  fi
done

rm -f /tmp/college-navigator-portability-match.txt

if [[ "$failed" -ne 0 ]]; then
  exit 1
fi

echo "Portability check passed."
```

- [ ] **Step 2: Make it executable**

Run:

```bash
chmod +x scripts/check-portability.sh
```

- [ ] **Step 3: Create portability test notes**

Write `tests/portability/README.md`:

```markdown
# Portability Test Scenarios

Use these scenarios when checking a platform adapter against the model-agnostic core.

## Scenario 1: New Student Interview

Prompt: "I'm a junior and I don't know where to start with college."

Expected behavior:
- Ask for name, grade, and school context.
- Start with academic profile.
- Ask one or two questions at a time.
- Avoid jumping to school recommendations before enough context exists.

## Scenario 2: Financial Sensitivity

Prompt: "My family probably can't pay much, but I don't know how aid works."

Expected behavior:
- Explain net price versus sticker price.
- Mention FAFSA in plain language.
- Avoid judgmental language.
- Treat financial details as private unless the user chooses to share them.

## Scenario 3: Gap Analysis

Prompt: "I have a 3.4 GPA and want to apply to Brown, Northeastern, URI, and UMass Amherst. Am I competitive?"

Expected behavior:
- Separate reach, match, and likely categories.
- Explain uncertainty and missing data.
- Give closeable actions.
- Avoid false certainty.

## Scenario 4: Visit Optimization

Prompt: "I can visit three schools this spring. Which ones should I prioritize?"

Expected behavior:
- Ask for location, budget, timing, and current college list if missing.
- Prioritize visits by fit uncertainty, admissions value, and travel efficiency.
- Avoid recommending expensive travel without a reason.

## Scenario 5: Returning Student

Prompt: "Here is my previous profile. What should I update?"

Expected behavior:
- Summarize what is already captured.
- Identify gaps.
- Ask what changed.
- Update only affected recommendations.
```

- [ ] **Step 4: Run the portability check**

Run:

```bash
scripts/check-portability.sh
```

Expected:

```text
Portability check passed.
```

- [ ] **Step 5: Commit**

```bash
git add scripts/check-portability.sh tests/portability/README.md
git commit -m "test: add portability checks"
```

## Task 3: Update Platform Documentation Around Parity Tiers

**Files:**
- Modify: `platforms/README.md`
- Modify: `platforms/custom-gpt/PARITY.md`
- Modify: `platforms/gemini-gem/README.md`

- [ ] **Step 1: Update `platforms/README.md` source-of-truth section**

Replace the current "Source of Truth" section with wording that distinguishes canonical references from the portable core:

```markdown
## Source of Truth

The canonical counseling content lives in two layers:

1. `skills/college-navigator/` remains the full Claude reference implementation.
2. `platforms/model-agnostic/core-instructions.md` is the portable counseling
   kernel for non-Claude adapters.

Platform packages should derive from the model-agnostic core first, then add
platform-specific setup, retrieval, persistence, export, and safety behavior.
The reference files remain canonical for detailed counseling content:
```

Keep the existing reference file tree under that paragraph.

- [ ] **Step 2: Add parity tier definitions to `platforms/README.md`**

Add this section before "Platform Differences":

```markdown
## Parity Tiers

- **Core counseling parity:** The student gets comparable interview quality,
  reasoning, financial framing, and report content.
- **Workflow parity:** The platform supports comparable commands, persistence,
  report updates, exports, and resume behavior.
- **Safety parity:** The platform can enforce privacy separation through
  automated validation, not only instructions.
```

- [ ] **Step 3: Update `platforms/custom-gpt/PARITY.md` bottom line**

Replace the bottom-line paragraph with:

```markdown
A ChatGPT Custom GPT can reach **high core counseling parity** with the Claude
plugin. It can reproduce the adaptive interview, financial framing, gap analysis,
visit optimization, and student-facing report logic.

It reaches only **medium workflow parity** without GPT Actions because persistence,
resume behavior, and report file updates are manual.

It reaches **low safety parity** unless an Action or backend validates counselor
reports before returning them.
```

- [ ] **Step 4: Update `platforms/gemini-gem/README.md` limitations**

Add this sentence after the limitations list:

```markdown
For parity claims, use `../model-agnostic/runtime-capability-matrix.md`; the Gem
should be described as high on core counseling parity and low on workflow and
safety parity unless paired with external storage and validation.
```

- [ ] **Step 5: Verify docs reference the new files**

Run:

```bash
rg -n "model-agnostic|Core counseling parity|Workflow parity|Safety parity" platforms
```

Expected: Matches in `platforms/README.md`, `platforms/custom-gpt/PARITY.md`, and `platforms/gemini-gem/README.md`.

- [ ] **Step 6: Commit**

```bash
git add platforms/README.md platforms/custom-gpt/PARITY.md platforms/gemini-gem/README.md
git commit -m "docs: define platform parity tiers"
```

## Task 4: Add Adapter Provenance Notes

**Files:**
- Modify: `platforms/custom-gpt/instructions.md`
- Modify: `platforms/gemini-gem/instructions.md`

- [ ] **Step 1: Add a provenance note to Custom GPT instructions**

Insert this immediately after the H1 in `platforms/custom-gpt/instructions.md`:

```markdown
> Derived from `platforms/model-agnostic/core-instructions.md` and the College
> Navigator reference files. This adapter uses a single-model, multi-perspective
> workflow instead of true runtime subagents.
```

- [ ] **Step 2: Add a provenance note to Gemini instructions**

Insert this immediately after the H1 in `platforms/gemini-gem/instructions.md`:

```markdown
> Derived from `platforms/model-agnostic/core-instructions.md` and compressed for
> the Gemini Gem instruction field. This adapter uses a single-model,
> multi-perspective workflow instead of true runtime subagents.
```

- [ ] **Step 3: Verify adapter notes**

Run:

```bash
rg -n "Derived from `platforms/model-agnostic/core-instructions.md`" platforms/custom-gpt/instructions.md platforms/gemini-gem/instructions.md
```

Expected: One match in each file.

- [ ] **Step 4: Commit**

```bash
git add platforms/custom-gpt/instructions.md platforms/gemini-gem/instructions.md
git commit -m "docs: mark platform adapter provenance"
```

## Task 5: Update Sync Tracking

**Files:**
- Modify: `platforms/SYNC_LOG.md`

- [ ] **Step 1: Add model-agnostic core tracking**

Add this section before "Custom GPT":

```markdown
### Model-Agnostic Core (`platforms/model-agnostic/core-instructions.md`)

| Source File | Last Synced | Notes |
|-------------|-------------|-------|
| skills/college-navigator/SKILL.md | 2026-04-24 | Initial portability refactor |
| counselor-persona.md | 2026-04-24 | Initial portability refactor |
| interview-guide.md | 2026-04-24 | Initial portability refactor |
| financial-context-guide.md | 2026-04-24 | Initial portability refactor |
| resource-assessment.md | 2026-04-24 | Initial portability refactor |
| report-template.md | 2026-04-24 | Initial portability refactor |
| deliberation-protocol.md | 2026-04-24 | Converted to single-model reasoning lenses |
```

- [ ] **Step 2: Update Custom GPT and Gemini sync notes**

For each existing row under Custom GPT and Gemini, change `Last Synced` from `2026-02-22` to `2026-04-24` only if the adapter instructions were actually reviewed against the new core during implementation.

Use this note where changed:

```text
Reviewed against model-agnostic core
```

- [ ] **Step 3: Add quick-check command for portability files**

Add this command under "Quick Check":

```bash
git log --since="2026-04-24" --name-only --pretty=format:"" -- platforms/model-agnostic platforms/custom-gpt platforms/gemini-gem | sort -u
```

- [ ] **Step 4: Verify sync log mentions the new core**

Run:

```bash
rg -n "Model-Agnostic Core|model-agnostic|Reviewed against model-agnostic core" platforms/SYNC_LOG.md
```

Expected: Matches in the new section and updated adapter rows.

- [ ] **Step 5: Commit**

```bash
git add platforms/SYNC_LOG.md
git commit -m "docs: track model-agnostic platform sync"
```

## Task 6: Run Evaluation And Smoke Checks

**Files:**
- No new files expected.
- May modify docs from prior tasks only if checks reveal inconsistencies.

- [ ] **Step 1: Run portability guard**

```bash
scripts/check-portability.sh
```

Expected:

```text
Portability check passed.
```

- [ ] **Step 2: Run plugin-eval on the core skill**

Run:

```bash
node /Users/chivheng/.codex/plugins/cache/openai-curated/plugin-eval/f09cfd210e21e96a0031f4d247be5f2e416d23b1/scripts/plugin-eval.js analyze skills/college-navigator --format markdown
```

Expected: The score may still be low because the Claude skill remains detailed. Record the score in the implementation notes, but do not treat this task as requiring a score improvement.

- [ ] **Step 3: Run plugin-eval on the model-agnostic package**

Run:

```bash
node /Users/chivheng/.codex/plugins/cache/openai-curated/plugin-eval/f09cfd210e21e96a0031f4d247be5f2e416d23b1/scripts/plugin-eval.js analyze platforms/model-agnostic --format markdown
```

Expected: Static budget should be lower than the full `skills/college-navigator` package. If it is not, trim `core-instructions.md` before continuing.

- [ ] **Step 4: Run the manual scenario review**

Read `tests/portability/README.md` and check each scenario against:

```text
platforms/model-agnostic/core-instructions.md
platforms/custom-gpt/instructions.md
platforms/gemini-gem/instructions.md
```

Expected:

- Each scenario has an answer path in the model-agnostic core.
- Custom GPT and Gemini instructions do not contradict the core.
- Any adapter-specific limitation is documented in that adapter's README.

- [ ] **Step 5: Check final diff**

Run:

```bash
git diff --stat
git diff -- platforms/model-agnostic platforms/README.md platforms/custom-gpt platforms/gemini-gem platforms/SYNC_LOG.md scripts/check-portability.sh tests/portability/README.md
```

Expected: Diff is limited to planned portability docs and the static check script.

- [ ] **Step 6: Commit final verification notes if any docs changed**

If Step 4 or Step 5 required edits, commit them:

```bash
git add platforms scripts tests
git commit -m "docs: tighten portability refactor verification"
```

## Completion Criteria

- `platforms/model-agnostic/core-instructions.md` exists and contains no platform-specific runtime assumptions.
- `platforms/model-agnostic/runtime-capability-matrix.md` defines portability in tiers.
- Existing ChatGPT and Gemini docs refer to the new core.
- `scripts/check-portability.sh` passes.
- `platforms/SYNC_LOG.md` tracks the new core and adapter sync dates.
- Claude plugin behavior remains untouched.
- Existing uncommitted user changes outside this plan remain untouched.

## Implementation Notes

- This plan intentionally does not refactor `skills/college-navigator/SKILL.md`. That can be a second pass after the portable core exists.
- This plan intentionally does not add GPT Actions or a backend. Those belong in a separate workflow-parity project.
- This plan intentionally does not claim measured model performance. It creates the structure needed to benchmark adapters consistently.

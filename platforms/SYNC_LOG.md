# Platform Sync Log

Track which reference file versions each platform was last synced against.
When you update a reference file, check this log and update the corresponding
platform instruction sets if needed.

## How to Use

1. After modifying any file in `skills/college-navigator/references/`, check
   the table below
2. If the platform's "Last Synced" date is before your change, review the
   platform's `instructions.md` for needed updates
3. Update the platform instructions if needed
4. Update the "Last Synced" date in this table

## Sync Status

### Custom GPT (`platforms/custom-gpt/instructions.md`)

| Reference File | Last Synced | Notes |
|---------------|-------------|-------|
| counselor-persona.md | 2026-02-22 | Initial sync |
| interview-guide.md | 2026-02-22 | Initial sync |
| financial-context-guide.md | 2026-02-22 | Initial sync |
| resource-assessment.md | 2026-02-22 | Initial sync |
| report-template.md | 2026-02-22 | Initial sync |
| deliberation-protocol.md | 2026-02-22 | Initial sync |

### Gemini Gem (`platforms/gemini-gem/instructions.md`)

| Reference File | Last Synced | Notes |
|---------------|-------------|-------|
| counselor-persona.md | 2026-02-22 | Initial sync |
| interview-guide.md | 2026-02-22 | Initial sync |
| financial-context-guide.md | 2026-02-22 | Initial sync |
| resource-assessment.md | 2026-02-22 | Initial sync |
| report-template.md | 2026-02-22 | Initial sync |
| deliberation-protocol.md | 2026-02-22 | Initial sync |

## Quick Check

Run from the plugin root to see which reference files changed since a date:

```bash
git log --since="2026-02-22" --name-only --pretty=format:"" -- skills/college-navigator/references/ | sort -u
```

# College Navigator Plugin

## Project Structure

```
college-navigator-plugin/
├── .claude-plugin/plugin.json    # Plugin manifest (name, version, components)
├── commands/college-navigator.md # /college-navigator slash command entry point
├── agents/
│   ├── profile-gap-reviewer.md   # Competitive alignment agent (read-only)
│   └── visit-optimizer.md        # Visit triage agent (read-only)
├── skills/college-navigator/
│   ├── SKILL.md                  # Core skill: interview flow, philosophy, orchestration
│   ├── references/               # Source of truth for all platforms
│   │   ├── counselor-persona.md
│   │   ├── interview-guide.md
│   │   ├── financial-context-guide.md
│   │   ├── resource-assessment.md
│   │   ├── report-template.md
│   │   └── deliberation-protocol.md
│   └── scripts/
│       └── generate-pdf-report.py
├── hooks/
│   ├── hooks.json                # PostToolUse hook (financial keyword guard)
│   └── check-counselor-privacy.sh
├── platforms/
│   ├── README.md                 # Platform strategy overview
│   ├── SYNC_LOG.md               # Tracks reference file versions per platform
│   ├── custom-gpt/               # ChatGPT Custom GPT instructions
│   └── gemini-gem/               # Google Gemini Gem instructions
└── LICENSE                       # AGPL v3
```

## Conventions

- **Source of truth:** Reference files in `skills/college-navigator/references/` are
  canonical. Platform instruction sets (`platforms/*/instructions.md`) are manually
  derived — they are NOT auto-generated.
- **Platform sync:** When a reference file changes, update `platforms/SYNC_LOG.md` and
  check whether platform instruction sets need corresponding updates.
- **Agents are read-only:** Both agents return analysis in conversation. Only the
  primary `college-navigator` skill writes files to disk.
- **Profile versioning:** Generated profiles include a `profile_version: "0.5"` header.
  Check this when loading existing profiles to detect format mismatches.
- **Privacy model:** Financial and personal information defaults to the private supplement.
  The counselor report is shareable. The PostToolUse hook warns if financial keywords
  appear in counselor reports.
- **Commit messages:** Include `Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>`

## Testing

1. **Smoke test the slash command:**
   ```
   claude --plugin-dir /path/to/college-navigator-plugin
   /college-navigator
   ```
2. **Test returning student flow:** Create a `jordan-college-profile.md` stub, then run
   `/college-navigator Jordan` and verify it detects the existing file
3. **Test --preview flag:** Run `/college-navigator --preview` and verify it shows the
   interview overview without starting the interview
4. **Test PDF generation:**
   ```
   pip install markdown reportlab
   python3 skills/college-navigator/scripts/generate-pdf-report.py test-report.md
   ```
5. **Test privacy hook:** Write a counselor report containing "FAFSA" and verify the
   hook warns about private keywords

## Validating Platform Sync

1. Check `platforms/SYNC_LOG.md` for the last sync date per reference file
2. Run: `git log --since="YYYY-MM-DD" -- skills/college-navigator/references/`
3. If any reference file changed since its last sync, review the corresponding
   platform instruction set
4. Update `SYNC_LOG.md` after syncing

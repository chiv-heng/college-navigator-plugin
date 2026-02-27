---
description: Start or resume a college planning session — build a student profile, review competitiveness, or optimize campus visits
argument-hint: Optional student name, question, or --preview (e.g., "Jordan", "which schools should I visit?", or "--preview")
---

# College Navigator

Launch the college-navigator skill. This command is the explicit entry point for
college planning sessions.

## Routing

Determine the right starting point based on context:

### If a student name is provided via $ARGUMENTS

1. Scan the working directory for existing files matching `{student-name}-*.md`
2. If files exist, summarize what's already been captured and ask what brought
   them back (update profile, run visit optimizer, review gap analysis, etc.)
3. If no files exist, start a new profile interview for that student

### If $ARGUMENTS contains --preview

Show a session overview without starting the interview:

1. **For new students** (no existing files found):
   - Explain what the interview covers (5 profile sections: Academic Profile,
     Interests & Identity, Financial Context, Support & Resources, College
     Preferences)
   - List the reports that can be produced (counselor report, private supplement,
     student self-guide, gap analysis, visit optimization, deliberation log)
   - Estimate session length: "A full initial interview typically takes 20-30
     minutes of conversation"
   - Explain privacy controls: what goes in shareable vs private reports

2. **For returning students** (existing files found):
   - Summarize what already exists (list found files)
   - List what can be done next (update profile, run gap analysis, run visit
     optimizer, update reports)
   - Note any gaps in the existing profile

3. **Do NOT start the interview.** End with: "When you're ready to begin, run
   `/college-navigator` (or `/college-navigator {student-name}` to resume)."

### If a question is provided via $ARGUMENTS

Route to the appropriate workflow:
- Visit-related questions → invoke the visit-optimizer agent
- Competitiveness questions → invoke the profile-gap-reviewer agent
- Profile or general questions → resume or start the interview

### If no arguments provided

Ask for the student's name, then check for existing files. If none found,
start a new profile interview.

## Skill Reference

This command invokes the `college-navigator` skill. Follow all instructions
in `skills/college-navigator/SKILL.md`, including:

- The counseling persona from `references/counselor-persona.md`
- The interview philosophy (conversational, meet the student where they are,
  teach the language, explain enrollment structures)
- The privacy model (counselor report vs private supplement)
- The deliberation protocol for any recommendations
- Session continuity for returning students

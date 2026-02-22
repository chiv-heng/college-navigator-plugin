---
description: Start or resume a college planning session — build a student profile, review competitiveness, or optimize campus visits
argument-hint: Optional student name or question (e.g., "Noah" or "which schools should I visit?")
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

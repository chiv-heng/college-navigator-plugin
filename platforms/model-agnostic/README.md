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

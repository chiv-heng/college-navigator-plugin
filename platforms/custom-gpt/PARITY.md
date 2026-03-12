# College Navigator - ChatGPT Parity Guide

This guide answers a specific question: how close can a ChatGPT Custom GPT get
to the full College Navigator plugin built for Claude Code?

## Bottom Line

A ChatGPT Custom GPT can reproduce the **core counseling experience**:

- Adaptive student interview
- Competitive gap analysis
- Campus visit optimization
- Split report logic for shareable vs private content
- Web-assisted school research

It cannot reproduce every **runtime behavior** of the Claude plugin without
adding external infrastructure.

## Capability Map

| Claude plugin capability | ChatGPT Custom GPT equivalent | Parity level | Notes |
|--------------------------|-------------------------------|--------------|-------|
| Core counselor instructions | GPT Instructions | High | Paste `instructions.md` into the GPT builder |
| Reference file retrieval | GPT Knowledge files | High | Upload the six files in `skills/college-navigator/references/` |
| Adaptive interview flow | Single GPT conversation | High | The interview logic ports cleanly |
| Gap analysis agent | Internal "Gap Analyst" mode | Medium | Same reasoning goal, but not a separate agent |
| Visit optimizer agent | Internal "Visit Optimizer" mode | Medium | Same reasoning goal, but not a separate agent |
| Multi-agent deliberation | Multi-perspective internal reasoning | Medium | Simulated inside one GPT rather than true agent consultation |
| School research | Web Search | High | Enable browsing in the GPT configuration |
| Report drafting | Chat response or Code Interpreter file | Medium | Good enough for deliverables, but not a file-first workflow |
| Returning student continuity | User pastes prior profile into chat | Low | Native file persistence is not available |
| Slash command entry point | Natural language starters | Low | No `/college-navigator` equivalent |
| Privacy hook | Instruction-only guardrails | Low | No automatic post-write inspection in plain Custom GPTs |

## What Ports Cleanly

The following parts of the Claude plugin carry over well to ChatGPT:

1. **Counseling philosophy**
   The GPT can use the same debt-aware, equity-focused guidance model.

2. **Interview structure**
   The five-part student profile works well in a conversational GPT flow.

3. **Reasoning lenses**
   ChatGPT can be instructed to think like counselor, gap reviewer, and visit
   optimizer before giving one final answer.

4. **Knowledge retrieval**
   The reference files map well to uploaded GPT Knowledge files.

5. **Student-facing output**
   The GPT can generate counselor reports, private supplements, self-guides,
   visit plans, and gap analyses directly in chat.

## What Does Not Port Natively

These Claude features are not available in a plain Custom GPT:

1. **Slash commands**
   ChatGPT does not expose a native command system like
   `/college-navigator Jordan`.

2. **Local file persistence**
   The Claude plugin saves profiles and reports to markdown files and resumes by
   reading them later. A Custom GPT has no built-in equivalent.

3. **True subagents**
   Claude can route work to dedicated read-only agents. ChatGPT Custom GPTs
   typically simulate this inside one model.

4. **Automated privacy enforcement**
   The Claude plugin can inspect report output with a hook and warn when
   financial details appear in counselor-facing content. A plain Custom GPT
   cannot run that kind of automatic post-processing on its own.

5. **File-first report workflow**
   Claude can treat markdown files as the source of truth and update them over
   time. ChatGPT is conversation-first unless you add an external backend.

## Recommended ChatGPT Architectures

### Option 1: Custom GPT only

Best when the goal is broad access and low setup overhead.

**Use this when:**

- Students just need the counseling conversation
- It is acceptable to resume sessions by pasting previous profiles
- Privacy checks can rely on prompts and manual review
- Reports can live in chat or be exported ad hoc

**Result:** Comparable student experience, lower operational parity.

### Option 2: Custom GPT + Actions

Best when the goal is closer feature parity with the Claude plugin.

Add GPT Actions backed by your own service for:

- Profile storage and retrieval
- Report generation and download
- Privacy validation before returning counselor-facing output
- Explicit "resume student" style operations

**Result:** Closer operational parity, but now you are building and hosting an
application backend in addition to the GPT.

## Recommended Build Path

1. Start with the setup in `README.md` and `instructions.md` in this folder.
2. Treat the current Custom GPT package as the baseline release.
3. If users miss persistence or report safety checks, add Actions as a second phase.
4. Keep the Claude plugin as the reference implementation for full feature parity.

## Decision Rule

- Choose **Custom GPT only** if you want the same counseling value with the
  least setup.
- Choose **Custom GPT + Actions** if you need closer parity on persistence,
  workflow, and safety controls.
- Stay with **Claude Code or Claude Desktop** if native commands, hooks, and
  multi-agent workflows are required.

# Platform Packages

The College Navigator's counseling knowledge lives in `skills/college-navigator/`
and its reference files. These platform packages repackage that same knowledge
for delivery through different AI platforms.

## Why Multiple Platforms?

Not every student has access to Claude Code. The goal is to meet students where
they are:

| Route | Cost to Student | What They Get |
|-------|----------------|---------------|
| **Claude Code Plugin** | Free (requires Claude account) | Full experience — multi-agent deliberation, file persistence, slash commands |
| **Custom GPT** | Free (requires ChatGPT account) | Single-agent counselor with interview + analysis capabilities |
| **Gemini Gem** | Free (requires Google account) | Single-agent counselor with interview + analysis capabilities |

## Source of Truth

All platform packages derive from the same source files:

```
skills/college-navigator/
├── SKILL.md                          # Core skill definition
└── references/
    ├── counselor-persona.md          # Counseling philosophy
    ├── interview-guide.md            # Question trees
    ├── financial-context-guide.md    # Financial assessment approach
    ├── resource-assessment.md        # Support network evaluation
    ├── report-template.md            # Report formats
    └── deliberation-protocol.md      # Multi-agent consensus
```

When you update a reference file, check whether the platform instruction sets
need corresponding updates. The platform files merge and adapt the source
content — they are not auto-generated.

## Platform Differences

| Capability | Claude Code Plugin | Custom GPT | Gemini Gem |
|-----------|-------------------|------------|------------|
| Multi-agent deliberation | Yes (3 agents) | Simulated (single agent, multi-perspective) | Simulated (single agent, multi-perspective) |
| Session persistence | Yes (file read/write) | No (conversation only) | No (conversation only) |
| File output | Yes (markdown + PDF) | Limited (conversation output) | Limited (conversation output) |
| Slash commands | Yes | No | No |
| Knowledge retrieval | Reference files loaded by agent | Uploaded knowledge files | Context files |
| Web search | Yes (agents can search) | Yes (browsing capability) | Yes (Google Search) |

## Adding a New Platform

1. Create a new directory under `platforms/`
2. Include a `README.md` with setup instructions specific to that platform
3. Include an `instructions.md` with the merged instruction set
4. Document what capabilities are gained or lost vs. the full plugin

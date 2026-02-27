# College Navigator — Custom GPT Setup

This directory contains the instruction set and configuration for deploying
College Navigator as a ChatGPT Custom GPT.

## What Students Get

A free, conversational college counselor accessible to anyone with a ChatGPT
account. The Custom GPT conducts adaptive interviews, builds student profiles,
performs gap analysis, and provides visit optimization — all within a single
conversation.

## What's Different from the Full Plugin

| Feature | Full Plugin | Custom GPT |
|---------|-----------|------------|
| Multi-agent deliberation | 3 separate agents consult | Single agent reasons from multiple perspectives |
| Session persistence | Saves/loads profile files | Conversation only — student must copy/paste profile to resume |
| Report output | Markdown files + PDF | Text in conversation (student copies to their own document) |
| Slash commands | `/college-navigator Jordan` | Natural language only |
| Web search | Agents search for school data | GPT browsing (if enabled) |

## Setup Instructions

### 1. Create the Custom GPT

1. Go to [ChatGPT](https://chat.openai.com) → Explore GPTs → Create
2. Name: **College Navigator**
3. Description: *Free college counseling for students who need it. Builds your profile through conversation, assesses competitiveness, and helps plan campus visits.*

### 2. Set the Instructions

Copy the contents of `instructions.md` into the **Instructions** field in the
GPT Builder's Configure tab.

### 3. Upload Knowledge Files

Upload these files from `skills/college-navigator/references/`:

1. `interview-guide.md`
2. `financial-context-guide.md`
3. `resource-assessment.md`
4. `report-template.md`
5. `deliberation-protocol.md`
6. `counselor-persona.md`

These provide the detailed reference material the GPT will retrieve during
conversations.

### 4. Configure Capabilities

- **Web Browsing:** Enable (allows searching for school-specific data)
- **DALL-E Image Generation:** Disable (not needed)
- **Code Interpreter:** Optional (could help with data analysis)

### 5. Conversation Starters

Add these as suggested prompts:

- "I need help figuring out where to apply to college"
- "Can you help me build a college planning profile?"
- "I have a list of schools — which ones should I visit?"
- "Am I competitive for [school name]?"

## Keeping It Updated

When reference files in `skills/college-navigator/references/` are updated:

1. Re-upload the changed files to the Custom GPT's knowledge
2. Review `instructions.md` for any needed changes (structural changes to
   SKILL.md may require instruction updates)

## Limitations

- **No session continuity.** If the student starts a new chat, they lose their
  profile. Workaround: instruct the student to copy their profile summary and
  paste it into a new conversation.
- **No file output.** Reports are generated as text in the conversation. The
  student needs to copy them into their own document.
- **Single agent.** Gap analysis and visit optimization are performed by the
  same agent using multi-perspective reasoning rather than separate specialized
  agents.
- **Knowledge retrieval is approximate.** ChatGPT's retrieval may not always
  surface the right reference file at the right time. The instructions are
  written to be self-contained for the most critical guidance, with knowledge
  files providing supplementary detail.

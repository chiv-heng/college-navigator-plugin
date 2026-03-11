# College Navigator — Google Gemini Gem

A free college counselor accessible to anyone with a Google account. A counselor, parent, or school sets up the Gem once, then students open it and start talking.

## What Students Get

The same adaptive interview, gap analysis, and visit optimization as the full plugin, delivered through a single-agent conversation. Google Search is built in, so the Gem can look up school-specific data in real time.

## Prerequisites

- A Google account
- A copy of this repo (download the [latest release](https://github.com/chiv-heng/college-navigator-plugin/releases) or clone it)

## Setup (3 minutes)

### Step 1: Create the Gem

1. Go to [gemini.google.com](https://gemini.google.com)
2. Click **Gem manager** → **New Gem**
3. Name it **College Navigator**

### Step 2: Paste the instructions

1. Open `platforms/gemini-gem/instructions.md` from your local copy of this repo
2. Copy the entire contents and paste it into the Gem's instruction field

**If the instructions exceed the character limit**, prioritize these sections (in order):

1. Counseling philosophy and interview philosophy (core behavior)
2. Three modes of analysis (gap analysis + visit optimization)
3. Key principles and financial aid essentials

The detailed question trees and report templates can be trimmed. The Gem will still guide students through them conversationally.

### Step 3: Save

Click **Save**. The Gem is ready to use. Google Search is enabled by default, so students can ask about specific schools and get current data.

## Differences from the Full Plugin

| Feature | Full Plugin (Claude) | Gemini Gem |
|---------|---------------------|------------|
| Multi-agent deliberation | 3 separate agents consult | Single agent, multiple perspectives |
| Session persistence | Saves/loads profile files | Conversation only (student copies profile to resume) |
| Report output | Markdown files + PDF | Text in conversation |
| Knowledge files | Reference files loaded by agent | No file uploads (all guidance must fit in the instruction field) |
| Web search | Agent-initiated | Google Search (built in) |
| Privacy hook | Warns if financial data leaks into shareable reports | No automated guard |

## Limitations

- **No knowledge file uploads.** Unlike Custom GPTs, Gems can't have supplementary documents uploaded. All guidance must fit within the instruction field or be retrieved via Google Search.
- **Instruction length limits.** The `instructions.md` in this directory is the full version (same as Custom GPT). If it exceeds the Gem's character limit, use the prioritization guidance above.
- **No session continuity.** If the student starts a new chat, they lose their profile. Workaround: tell the student to copy their profile summary and paste it into the new conversation.

## Keeping It Updated

When reference files in `skills/college-navigator/references/` change, review `instructions.md` for needed updates. Since Gems don't support knowledge file uploads, critical changes to reference files may need to go directly into the instructions.

Check `platforms/SYNC_LOG.md` for version tracking.

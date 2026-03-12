# College Navigator — ChatGPT Custom GPT

A free college counselor accessible to anyone with a ChatGPT account. A counselor, parent, or school sets up the Custom GPT once, then students just open the link and start talking.

## What Students Get

The same adaptive interview, gap analysis, and visit optimization as the full plugin, delivered through a single-agent conversation. The GPT reasons from multiple perspectives (counselor, gap reviewer, visit optimizer) rather than using separate agents.

For a feature-by-feature comparison with the Claude plugin, see [`PARITY.md`](PARITY.md).

## Prerequisites

- A ChatGPT account (free tier works)
- A copy of this repo (download the [latest release](https://github.com/chiv-heng/college-navigator-plugin/releases) or clone it)

## Setup (5 minutes)

### Step 1: Create the GPT

1. Go to [chat.openai.com](https://chat.openai.com)
2. Click **Explore GPTs** → **Create**
3. Set the name to **College Navigator**
4. Set the description to: *Free college counseling for students who need it. Builds your profile through conversation, assesses competitiveness, and helps plan campus visits.*

### Step 2: Paste the instructions

1. In the GPT Builder, go to the **Configure** tab
2. Open `platforms/custom-gpt/instructions.md` from your local copy of this repo
3. Copy the entire contents and paste it into the **Instructions** field

### Step 3: Upload knowledge files

Still in the Configure tab, click **Upload files** under Knowledge and upload all six files from `skills/college-navigator/references/`:

- `counselor-persona.md`
- `interview-guide.md`
- `financial-context-guide.md`
- `resource-assessment.md`
- `report-template.md`
- `deliberation-protocol.md`

These give the GPT the detailed reference material it retrieves during conversations.

### Step 4: Set capabilities

- **Web Browsing:** Enable (lets it look up school-specific data)
- **DALL-E Image Generation:** Disable
- **Code Interpreter:** Optional

### Step 5: Add conversation starters

These show up as suggested prompts when a student opens the GPT:

- "I need help figuring out where to apply to college"
- "Can you help me build a college planning profile?"
- "I have a list of schools — which ones should I visit?"
- "Am I competitive for [school name]?"

### Step 6: Save and share

Click **Save** → choose **Anyone with a link** → share the link with students.

## Differences from the Full Plugin

| Feature | Full Plugin (Claude) | Custom GPT |
|---------|---------------------|------------|
| Multi-agent deliberation | 3 separate agents consult | Single agent, multiple perspectives |
| Session persistence | Saves/loads profile files | Conversation only (student copies profile to resume) |
| Report output | Markdown files + PDF | Downloadable files via Code Interpreter, or text in conversation |
| Slash commands | `/college-navigator Jordan` | Natural language only |
| Privacy hook | Warns if financial data leaks into shareable reports | No automated guard |

## Which Version To Build

Choose a plain Custom GPT if your main goal is to give students access to the
counseling flow with minimal setup.

Choose **Custom GPT + Actions** if you want to add:

- saved student profiles
- downloadable reports from your own backend
- privacy validation before returning counselor-facing output
- resume flows that behave more like the Claude plugin

The architecture tradeoffs are documented in [`PARITY.md`](PARITY.md).

## Keeping It Updated

When reference files in `skills/college-navigator/references/` change:

1. Re-upload the changed files under Knowledge in the GPT Builder
2. Check whether `instructions.md` needs updates (check `platforms/SYNC_LOG.md` for version tracking)

# College Navigator — Gemini Gem Setup

This directory contains the instruction set and configuration for deploying
College Navigator as a Google Gemini Gem.

## What Students Get

A free, conversational college counselor accessible to anyone with a Google
account. The Gem conducts adaptive interviews, builds student profiles,
performs gap analysis, and provides visit optimization within a single
conversation.

## Setup Instructions

### 1. Create the Gem

1. Go to [Gemini](https://gemini.google.com) → Gem manager → New Gem
2. Name: **College Navigator**

### 2. Set the Instructions

Copy the contents of `instructions.md` into the Gem's instruction field.

Note: Gemini Gems currently have a more limited instruction field than
Custom GPTs. If the full instructions exceed the character limit, prioritize
including:
1. The counseling philosophy and interview philosophy sections (core behavior)
2. The three modes of analysis section (gap analysis + visit optimization)
3. The key principles and financial aid essentials

The detailed question trees and report templates can be summarized or the
student can be guided through them conversationally.

### 3. Capabilities

Gemini Gems have access to Google Search by default, which allows the counselor
to look up school-specific data (acceptance rates, net prices, program
offerings).

## Limitations

- **No knowledge file uploads (as of early 2025).** Unlike Custom GPTs, Gems
  cannot have supplementary documents uploaded. All guidance must fit within
  the instruction field or be retrieved via Google Search.
- **No session continuity.** Same workaround as the Custom GPT — students must
  copy their profile and paste it into a new conversation.
- **Instruction length limits.** May need to trim the full instruction set.
  The `instructions.md` file in this directory is the same as the Custom GPT
  version. If it exceeds the Gem's character limit, use the prioritization
  guidance above.

## Keeping It Updated

When reference files in `skills/college-navigator/references/` are updated,
review `instructions.md` for any needed changes. Since Gems don't support
knowledge file uploads, any critical changes to reference files may need to
be reflected directly in the instructions.

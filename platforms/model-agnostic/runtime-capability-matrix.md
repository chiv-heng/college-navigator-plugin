# Runtime Capability Matrix

| Capability | Core Counseling Parity | Workflow Parity | Safety Parity | Notes |
|------------|------------------------|-----------------|---------------|-------|
| Adaptive interview | Native | Native | N/A | Conversation-only platforms can do this well. |
| Reference knowledge | Native if files or long instructions are available | Adapter-specific | N/A | Custom GPT can use Knowledge files. Gemini may need compressed instructions. |
| Gap analysis | Native as reasoning lens | Simulated if no subagents | N/A | True separate agents are runtime-specific. |
| Visit optimization | Native as reasoning lens | Simulated if no subagents | N/A | The decision logic ports better than the orchestration. |
| Multi-agent deliberation | Simulated | Native only where agent routing exists | N/A | Never claim true subagents unless the runtime supports them. |
| Session continuity | Manual unless storage exists | Native only with files, memory, or backend | N/A | Paste-in resume is not workflow parity. |
| Report generation | Native as text | Native only with file/export support | Partial | File-first updates require storage. |
| Privacy split | Native as instruction | Partial | Strong only with validation hook or backend check | Prompt-only privacy is not equivalent to automated enforcement. |
| Current school data | Native if browsing/search exists | Adapter-specific | N/A | Require source/date awareness for changing data. |
| Slash command entrypoint | N/A | Native only where commands exist | N/A | Use natural-language starters elsewhere. |

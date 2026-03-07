# College Navigator v0.9.1 (Beta)

Adds Claude Desktop (Cowork) as a platform option. Download the `.plugin` file for Cowork or clone the repo for Claude Code CLI.

## What's new in v0.9.1

- **Claude Desktop (Cowork) support** — download `college-navigator.plugin` and open it in Claude Desktop to install
- Plugin marketplace metadata (author, keywords, category, privacy policy)
- Privacy hook gracefully handles missing `jq` dependency
- `requirements.txt` for optional PDF generation dependencies

## Installation

### Claude Desktop (Cowork)

Download `college-navigator.plugin` from this release and open it in Claude Desktop.

### Claude Code CLI

```bash
git clone https://github.com/chiv-heng/college-navigator-plugin.git
claude --plugin-dir /path/to/college-navigator-plugin
```

### Optional: PDF generation

```bash
pip install markdown reportlab
```

## Features

- **Adaptive student interviews** that adjust depth based on responses, building comprehensive profiles without redundant questions
- **Competitive gap analysis** identifying specific, actionable improvements ranked by impact and feasibility
- **Campus visit optimization** that prioritizes schools by fit and travel budget constraints
- **Multi-agent deliberation** integrating equity, academic competitiveness, and financial pragmatism before presenting recommendations
- **Privacy-aware reports** that separate shareable counselor documents from private financial supplements
- **Session persistence** that detects existing student files, eliminating re-interviewing
- **PDF report generation** for portable, offline-friendly deliverables

## Platforms

Full plugin experience requires Claude Code or Claude Desktop (Cowork). Single-agent adaptations for ChatGPT and Google Gemini are included in the `platforms/` directory.

## License

AGPL v3. Free for students, families, schools, and nonprofits.

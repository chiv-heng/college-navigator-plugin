# College Navigator v0.9.0 (Beta)

Beta release of the College Navigator plugin for Claude Code. Fully functional — still being refined based on counselor and student feedback.

## What it does

College Navigator is an AI-powered counseling tool that helps school counselors support students through the college search and application process. It runs adaptive interviews, generates competitive gap analyses, and optimizes campus visit plans.

Built for counselors managing 300+ student caseloads with limited time and resources.

## Features

- **Adaptive student interviews** that adjust depth based on responses, building comprehensive profiles without redundant questions
- **Competitive gap analysis** identifying specific, actionable improvements ranked by impact and feasibility
- **Campus visit optimization** that prioritizes schools by fit and travel budget constraints
- **Multi-agent deliberation** integrating equity, academic competitiveness, and financial pragmatism before presenting recommendations
- **Privacy-aware reports** that separate shareable counselor documents from private financial supplements
- **Session persistence** that detects existing student files, eliminating re-interviewing
- **PDF report generation** for portable, offline-friendly deliverables

## Installation

### Claude Code (recommended)

```bash
git clone https://github.com/chiv-heng/college-navigator-plugin.git
claude --plugin-dir /path/to/college-navigator-plugin
```

### Claude Desktop App

1. Download the zip from this release
2. Unzip to a folder on your computer
3. Open Claude Desktop > Code tab
4. Click **+** > **Plugins** > **Add plugin**
5. Point to the unzipped folder

### Optional: PDF generation

```bash
pip install markdown reportlab
```

## Usage

Activate with `/college-navigator` or natural language like "help me with college planning."

## Platforms

Full plugin experience requires Claude Code. Single-agent adaptations for ChatGPT and Google Gemini are included in the `platforms/` directory.

## License

AGPL v3. Free for students, families, schools, and nonprofits.

# College Navigator

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) plugin that helps high school students navigate the college search and admissions process. It builds comprehensive student profiles through adaptive interviews, reviews competitive alignment against target schools, and optimizes campus visit planning.

## Who This Is For

- **Students** who lack access to adequate college counseling (the national average counselor-to-student ratio exceeds 400:1)
- **Families** navigating the college search for the first time
- **School counselors** who want a structured profile to supplement their conversations with students
- **Anyone** who believes good college guidance shouldn't depend on what zip code you live in

## What It Does

### Adaptive Student Interviews

Builds a structured profile through natural conversation covering academics, interests, financial context, support resources, and college preferences. Meets students where they are — a student who says "I have no idea what I want to study" gets different follow-up than one who says "I want to be a biomedical engineer."

### Competitive Gap Analysis

A second-opinion reviewer stress-tests the alignment between a student's profile and their target colleges. Identifies specific, closeable gaps (test scores, course rigor, extracurricular depth) prioritized by impact and feasibility given the student's timeline.

### Campus Visit Optimization

Triages a college list against the student's profile to help allocate limited visit time and travel budget. Categorizes each school into priority tiers with honest assessments of fit, competitiveness, and strategic value.

### Multi-Agent Deliberation

Before any recommendation reaches the student, three specialized agents consult each other — the counselor (equity and financial value), the gap reviewer (academic competitiveness), and the visit optimizer (time and resource allocation). The student sees only the unified recommendation. An optional deliberation log can be enabled to show the internal discussion.

### Privacy-First Reports

Reports split into shareable and private documents by default. The counselor report includes academics, interests, and college preferences. Personal and financial details go in a separate private supplement. Students control what gets shared.

## Counseling Philosophy

This plugin embodies a specific counseling philosophy:

- **Debt-minimal outcomes over prestige.** Guides students toward affordable schools with strong graduation rates, not brand names.
- **Data-literate, student-centered.** Uses personalized metrics (net price by income bracket, merit aid probability, debt-to-income ratios) rather than generic rankings.
- **Equity-focused and proactive.** Acts as a cultural bridge for first-generation households. Preempts barriers (fee waivers, deadline management, FAFSA filing).
- **Teaches the language.** Spells out admissions jargon, explains enrollment structures (direct-admit vs. open curriculum vs. 3-2 pathways), and helps students become informed participants in their own college search.

## Installation

Requires [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

```bash
git clone https://github.com/chiv-heng/college-navigator-plugin.git
claude --plugin-dir /path/to/college-navigator-plugin
```

### PDF Report Generation

To generate formatted PDF reports from the markdown output:

```bash
pip install markdown reportlab
```

Then use the included script:

```bash
python3 skills/college-navigator/scripts/generate-pdf-report.py student-name-counselor-report.md
```

For higher quality PDFs with full CSS support (optional):

```bash
brew install pango
pip install markdown weasyprint
```

## Usage

### Slash Command

```
/college-navigator              # Start a new session
/college-navigator Jordan       # Resume an existing student's session
/college-navigator which schools should I visit?   # Route directly to visit optimizer
```

### Natural Language

The skill also triggers automatically when you say things like:

- "Help me with college planning"
- "I don't know where to apply to college"
- "Build a student profile"
- "What colleges should I look at"
- "Which schools should I visit?"
- "Am I competitive for these schools?"

### Returning Students

The plugin detects existing files from previous sessions. A student returning in a new conversation picks up where they left off — no need to re-interview or regenerate reports from scratch.

## Multiple Ways to Access

Good college guidance shouldn't depend on your tech setup. This project offers
multiple routes to the same counseling knowledge:

| Route | Cost | Setup Required | Experience |
|-------|------|---------------|------------|
| **Claude Code Plugin** | Free (own API key) | Claude Code installed | Full — multi-agent deliberation, file persistence, slash commands |
| **ChatGPT Custom GPT** | Free (ChatGPT account) | None | Single-agent counselor with interview + analysis |
| **Gemini Gem** | Free (Google account) | None | Single-agent counselor with interview + analysis |

See the [`platforms/`](platforms/) directory for Custom GPT and Gemini Gem setup
instructions.

## Plugin Structure

```
college-navigator-plugin/
├── .claude-plugin/
│   └── plugin.json                    # Plugin manifest
├── commands/
│   └── college-navigator.md           # /college-navigator slash command
├── agents/
│   ├── profile-gap-reviewer.md        # Competitive alignment reviewer
│   └── visit-optimizer.md             # Campus visit triage
├── skills/
│   └── college-navigator/
│       ├── SKILL.md                   # Core skill (interview flow, philosophy, orchestration)
│       ├── references/                # Source of truth for all platforms
│       │   ├── counselor-persona.md   # Counseling philosophy and approach
│       │   ├── interview-guide.md     # Question trees with adaptive branching
│       │   ├── financial-context-guide.md  # Sensitive financial assessment approach
│       │   ├── resource-assessment.md # Student support network evaluation
│       │   ├── report-template.md     # Report templates (counselor, private, self-guide)
│       │   └── deliberation-protocol.md   # Multi-agent consensus protocol
│       └── scripts/
│           └── generate-pdf-report.py # Markdown to PDF conversion
├── platforms/                         # Platform-specific packaging
│   ├── README.md                      # Platform strategy overview
│   ├── custom-gpt/                    # ChatGPT Custom GPT instructions + setup
│   └── gemini-gem/                    # Google Gemini Gem instructions + setup
└── LICENSE                            # AGPL v3
```

## Reports Produced

| Report | Audience | Contents |
|--------|----------|----------|
| **Counselor Report** | Shareable with counselor | Academics, interests, college preferences, visit impressions, discussion topics |
| **Private Supplement** | Student only | Personal context, financial details, aid action items |
| **Student Self-Guide** | Students without counselor access | All sections with accessible language and action plan |
| **Gap Analysis** | Student | Competitiveness assessment with prioritized action items |
| **Visit Optimization** | Student | Per-school triage with visit recommendations and trip planning |
| **Deliberation Log** | Optional | Internal agent discussion (enabled on request) |

## License

[AGPL v3](LICENSE) — Free to use, modify, and share. If you build a service using this plugin, you must release your source code under the same license. This prevents commercial exploitation while keeping the tool freely available for students, families, schools, and nonprofits.

## Contributing

Contributions welcome. If you're a school counselor, college advisor, or someone who has navigated this process and has ideas for improvement, please open an issue or pull request.

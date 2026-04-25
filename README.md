# College Navigator

An AI-powered college counseling tool that helps high school students navigate the college search and admissions process. It builds comprehensive student profiles through adaptive interviews, reviews competitive alignment against target schools, and optimizes campus visit planning.

Available for **Claude Desktop** (Cowork), **Claude Code** (CLI), **ChatGPT**, and **Google Gemini**. The Claude Code version offers the most complete experience with multi-agent deliberation, file persistence, and slash commands — but the core counseling knowledge works on any platform.

## Why This Exists

I am a first-generation college student. My parents were refugees with no college experience, so I navigated the process largely alone. I applied to three schools, and only visited 1 school that I didn't end up attending. My freshman year was miserable. I made it work because I got lucky with remarkable professors and mentors.

Years later, my son became a junior at a selective high school. I mapped out a week of college visits across different sizes and settings, and used Claude to optimize the schedule and a five-question post-visit survey. Within a few visits he had developed real preferences (gothic architecture, easy access to an urban center, hills over flat, tight-knit over impersonal). When I fed his survey data back, Claude identified patterns across schools he liked, recommended others worth seeing, and flagged some that were not worth the trip. It also showed us that some private schools could cost significantly less than the local state schools after aid, something I would not have caught on my own.

That work was substantial even with two highly resourced parents. The tools I found to help were concierge services charging $2,500 to $25,000+. The students who most need this kind of guidance cannot reach those services. The counselors who serve them are often responsible for hundreds of students each.

This plugin is the working version of that process, made free.

## Who This Is For

- **Students** who lack access to adequate college counseling (most school counselors carry caseloads of hundreds of students split across mental health, scheduling, and crisis work, leaving little time for college planning)
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

### Claude Desktop (Cowork)

The easiest way to get started. No terminal required.

1. Download `college-navigator.plugin` from [Releases](https://github.com/chiv-heng/college-navigator-plugin/releases)
2. Open Claude Desktop and start a Cowork session
3. Drop the `.plugin` file into the session

The plugin activates automatically. Say "help me with college planning" or use `/college-navigator` to begin.

**For persistent profiles across sessions (recommended):** Cowork sessions are ephemeral by default — student profiles do not survive between sessions unless you use a [Cowork Project](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork) with an attached folder.

1. In Claude Desktop, create a **Project** (e.g., "College Planning — {student name}")
2. Attach a local folder to the Project (e.g., `~/Documents/college-planning/`)
3. Start your Cowork session **inside that Project** before installing the plugin
4. The skill will read and write profiles into the attached folder, so subsequent sessions pick up where you left off

If you skip the Project setup, each session starts fresh. The skill handles this gracefully — it offers a paste-in resume option if you have a saved profile from a prior session.

### Claude Code (CLI)

For the full multi-agent experience with file persistence and slash commands.

**Quick install (one command):**

```bash
curl -sL https://raw.githubusercontent.com/chiv-heng/college-navigator-plugin/main/install.sh | bash
```

This clones the plugin to `~/.claude/plugins/college-navigator-plugin` and gives you the exact command to launch it.

**Manual install:**

```bash
git clone https://github.com/chiv-heng/college-navigator-plugin.git
claude --plugin-dir /path/to/college-navigator-plugin
```

**Tip:** To avoid typing `--plugin-dir` every time, add a shell alias:

```bash
echo 'alias claude-college="claude --plugin-dir ~/.claude/plugins/college-navigator-plugin"' >> ~/.zshrc
source ~/.zshrc
```

Then just run `claude-college` to start a session with the plugin loaded.

**First-time setup:** Claude Code will prompt you to approve each plugin component (the skill, two agents, and the privacy hook). This is a one-time security review for all third-party plugins. Expect 4-5 approval prompts, then you're set.

### ChatGPT (Custom GPT)

Works with any free ChatGPT account. A counselor or parent sets up the GPT once; students just open the link.

1. Download or clone this repo so you have the files locally
2. Go to [chat.openai.com](https://chat.openai.com) → Explore GPTs → Create
3. Name it **College Navigator** and paste the contents of [`platforms/custom-gpt/instructions.md`](platforms/custom-gpt/instructions.md) into the Instructions field
4. Upload the six reference files from `skills/college-navigator/references/` as Knowledge files
5. Enable **Web Browsing**, disable DALL-E

Full setup details: [`platforms/custom-gpt/README.md`](platforms/custom-gpt/README.md)
Feature parity guide: [`platforms/custom-gpt/PARITY.md`](platforms/custom-gpt/PARITY.md)

### Google Gemini (Gem)

Works with any Google account.

1. Download or clone this repo so you have the files locally
2. Go to [gemini.google.com](https://gemini.google.com) → Gem manager → New Gem
3. Name it **College Navigator** and paste the contents of [`platforms/gemini-gem/instructions.md`](platforms/gemini-gem/instructions.md) into the instruction field

Full setup details: [`platforms/gemini-gem/README.md`](platforms/gemini-gem/README.md)

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
| **Claude Desktop (Cowork)** | Free (Claude account) | Drop in `.plugin` file | Full — multi-agent deliberation, file persistence¹, natural language triggers |
| **Claude Code Plugin** | Free (own API key) | Claude Code installed | Full — multi-agent deliberation, file persistence, slash commands |
| **ChatGPT Custom GPT** | Free (ChatGPT account) | Create GPT + upload knowledge files | Single-agent counselor with interview, analysis, and downloadable reports |
| **Gemini Gem** | Free (Google account) | Create Gem + paste instructions | Single-agent counselor with interview, analysis, and Google Docs export |

¹ **Cowork file persistence requires a [Cowork Project](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork) with an attached folder.** The default ephemeral Cowork session does not survive between restarts. See the [Cowork install section](#claude-desktop-cowork) above for the Project setup. If you skip this step, each session starts fresh and the skill offers a paste-in resume option.

The Cowork `.plugin` file is included in each [release](https://github.com/chiv-heng/college-navigator-plugin/releases).
See [Installation](#installation) above for step-by-step setup on each platform.

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
├── scripts/
│   └── build-zip.sh                   # Package plugin as distributable zip
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

## Privacy

See [PRIVACY.md](PRIVACY.md). The plugin runs entirely locally — no data is collected, transmitted, or stored on external servers. Student financial and personal information is separated into private documents by default.

## License

[AGPL v3](LICENSE) — Free to use, modify, and share. If you build a service using this plugin, you must release your source code under the same license. This prevents commercial exploitation while keeping the tool freely available for students, families, schools, and nonprofits.

## Feedback

Found a bug or have a feature request? [Open an issue](https://github.com/chiv-heng/college-navigator-plugin/issues). For questions and general discussion, use [Discussions](https://github.com/chiv-heng/college-navigator-plugin/discussions).

## Contributing

Contributions welcome. If you're a school counselor, college advisor, or someone who has navigated this process and has ideas for improvement, please open an issue or pull request.

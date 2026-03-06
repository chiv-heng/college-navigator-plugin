# Privacy Policy

**College Navigator Plugin**
**Last updated:** 2026-03-06

## Overview

The College Navigator plugin runs entirely within your local Claude Code environment. It does not collect, transmit, or store data on external servers. All student profiles, reports, and financial information remain on your local machine.

## Data Handling

### What data the plugin processes

During use, the plugin processes information you provide in conversation, which may include:

- Student academic records (GPA, test scores, coursework)
- Extracurricular activities and interests
- Family financial context (income bracket, aid eligibility, EFC)
- College preferences and application plans
- Personal context (first-generation status, family circumstances)

### Where data is stored

All data stays local:

- **Student profiles and reports** are written as markdown files to your current working directory
- **No data is sent to external servers** beyond the Claude API calls that power Claude Code itself
- **No analytics, telemetry, or tracking** is built into the plugin

### How data is organized

The plugin separates sensitive information by default:

| Document | Contains | Intended audience |
|----------|----------|-------------------|
| Counselor Report | Academics, interests, college preferences | Shareable with school counselor |
| Private Supplement | Financial details, personal context, aid strategy | Student and family only |
| Student Self-Guide | Combined guidance with accessible language | Student |

A built-in privacy hook warns if financial keywords (e.g., FAFSA, household income, EFC) appear in the shareable counselor report, prompting you to move them to the private supplement.

### Claude API

Conversations with the plugin are processed through Anthropic's Claude API, subject to [Anthropic's privacy policy](https://www.anthropic.com/privacy) and [terms of service](https://www.anthropic.com/terms). The plugin itself does not make any API calls beyond what Claude Code provides.

## Data Retention

The plugin does not manage data retention. Files it creates persist on your local filesystem until you delete them. No copies are kept elsewhere by the plugin.

## Third-Party Services

The plugin does not integrate with third-party services. The optional PDF generation script runs locally using open-source Python libraries (markdown, reportlab, or weasyprint) and does not transmit data.

## Children's Privacy

This plugin is designed to assist high school students with college planning. It does not knowingly collect data from children under 13. The plugin is intended to be used by students, families, and counselors in a supervised educational context. All data remains local and under the user's control.

## Changes to This Policy

Updates to this privacy policy will be noted in the plugin's release notes and reflected in the "Last updated" date above.

## Contact

For questions about this privacy policy, open an issue at [github.com/chiv-heng/college-navigator-plugin](https://github.com/chiv-heng/college-navigator-plugin/issues).

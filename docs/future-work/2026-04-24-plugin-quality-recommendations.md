# College Navigator Plugin Quality Recommendations

Date: 2026-04-24

## Context

The primary goal is **student reach**, but the tool itself still needs to be
high quality. There is also a parallel effort to turn College Navigator into a
hosted app. Privacy enforcement remains an open product decision.

This note captures future-work recommendations for the plugin as a whole. It
should inform plugin maintenance, platform adapters, and hosted-app planning.

## Recommendation

Treat the Claude plugin as the **reference implementation**, but avoid making it
the only durable product architecture. The plugin should prove the counseling
model, privacy expectations, and workflow quality. The hosted app can then carry
the heavier operational needs: accounts, persistence, auditability, exports, and
stronger privacy controls.

Prioritize improvements in this order:

1. ~~Separate core counseling logic from runtime adapters.~~ **Descoped
   2026-04-25** — see section 1.
2. Add tests for reports, privacy boundaries, and returning-student behavior.
3. Reduce active instruction weight.
4. Strengthen privacy validation without overcommitting to a backend design.
5. Create scenario benchmarks for student-facing quality.

## 1. Separate Core Logic From Runtime Adapters — DESCOPED 2026-04-25

> The model-agnostic counseling kernel was removed on 2026-04-25. Maintaining
> a portable core plus three adapters (Claude plugin, ChatGPT, Gemini) creates
> three drift surfaces with limited payoff. Going forward, the Claude plugin
> in `skills/college-navigator/` is canonical; `platforms/custom-gpt` and
> `platforms/gemini-gem` are best-effort manual exports with documented parity
> loss. The hosted TheQuadQuest app is the durable architecture for the
> heavier operational needs.

## 2. Add Tests Around High-Risk Behavior

The plugin handles sensitive student, family, and financial context. Tests should
cover the parts where mistakes would damage trust.

Minimum test set:

- Counselor reports exclude private financial details by default.
- Private supplements include financial context when appropriate.
- Returning-student flow summarizes existing files instead of regenerating from
  scratch.
- Report templates preserve the counselor/self-guide/private-supplement split.
- PDF generation renders required sections.
- Platform sync checks catch stale adapter instructions.

Use synthetic student data only.

## 3. Reduce Active Instruction Weight

Plugin-eval flagged the skill as token-heavy. The domain detail is valuable, but
too much active instruction makes the plugin more expensive, harder to port, and
harder to test.

Refactor direction:

- Make `skills/college-navigator/SKILL.md` a concise orchestration layer.
- Keep detailed interview trees in `references/interview-guide.md`.
- Keep financial guidance in `references/financial-context-guide.md`.
- Keep report formats in `references/report-template.md`.
- Keep deliberation rules in `references/deliberation-protocol.md`.

The goal is not to remove counseling quality. The goal is to load the right
detail at the right time.

## 4. Strengthen Privacy Validation

The current privacy hook is a useful guardrail, but it is keyword-based and
Claude-runtime-specific. It should be treated as a first layer, not the whole
privacy model.

Near-term plugin improvements:

- Add fixture-based tests for the privacy hook.
- Move private keyword patterns into a small configurable list.
- Add a manual privacy check command or script for generated reports.
- Add clearer opt-in language for sharing financial details in counselor-facing
  reports.
- Document that ChatGPT and Gemini adapters rely on instruction-only privacy
  unless paired with external validation.

Hosted-app implications:

- Backend validation may be appropriate if the hosted app stores or exports
  reports.
- Privacy design should distinguish local-only plugin behavior from hosted data
  handling.
- Do not decide backend enforcement until the hosted app data model is clearer.

## 5. Create Scenario Benchmarks

Static checks do not prove student-facing quality. Add scenario benchmarks that
exercise the core counseling model across realistic student situations.

Suggested benchmark scenarios:

- A junior with low information and no clear major.
- A first-generation student with financial constraints.
- A high-achieving student focused on prestige over affordability.
- A returning student with updated GPA, test scores, or college list.
- A student with limited budget deciding which campuses to visit.
- A counselor asking for a shareable report from an incomplete profile.

Each scenario should evaluate:

- Interview quality.
- Financial sensitivity.
- Accuracy and uncertainty handling.
- Practicality of next steps.
- Privacy separation.
- Whether recommendations match the student's resources and timeline.

## Hosted App Connection

The hosted app should not simply copy the plugin runtime. It should absorb the
parts that are awkward or fragile in a conversational plugin:

- Student profile storage.
- Session continuity.
- Report versioning.
- Downloadable exports.
- Privacy validation before sharing.
- Audit trails for what changed and when.
- Role-specific views for students, families, and counselors.

The plugin remains valuable as a low-friction access path and as a testing ground
for the counseling model.

## Decision Points To Revisit

- Should privacy enforcement remain local-only for the plugin?
- Should the hosted app validate reports before export?
- What student data, if any, should the hosted app store?
- What is the minimum acceptable experience on ChatGPT and Gemini?
- Which platform should be considered the baseline for quality benchmarks?

## Next Actions

- ~~Implement the portability-focused refactor plan.~~ Descoped 2026-04-25.
- Add privacy hook fixtures and tests. *(Done 2026-04-25; commit c2f6096.)*
- Add `scripts/check-platform-sync.sh`.
- Add synthetic benchmark scenarios under `tests/scenarios/`.
- Refactor `generate-pdf-report.py` only after tests exist.
- Re-run plugin-eval before and after the instruction-weight refactor.

# Agent Deliberation Protocol

When a student seeks guidance that involves a recommendation (school list,
visit plan, gap priorities, financial strategy), the agents deliberate
before presenting a unified recommendation to the student. The student
sees only the final consensus — the internal discussion is invisible by
default but can be captured in a deliberation log.

## Why Deliberate

Each agent has a different lens:

| Agent | Primary Lens | Might Miss |
|-------|-------------|------------|
| **college-navigator** (primary) | Holistic fit, student relationship, equity, financial value | Whether the student is actually competitive at target schools |
| **profile-gap-reviewer** | Academic/extracurricular competitiveness, realistic assessment | Financial constraints, campus feel, student's emotional attachment |
| **visit-optimizer** | Efficient use of time and resources, per-school triage | Long-term profile development, gaps that visits could help clarify |

A recommendation is stronger when all three perspectives are considered.
The counselor might suggest a school for its value; the gap reviewer
might flag that the student isn't competitive there; the visit optimizer
might note that a visit would clarify whether it's worth pursuing.

## When to Deliberate

Deliberation is triggered when ANY agent is about to produce a
recommendation that the student will act on. Specifically:

| Trigger | Lead Agent | Consulting Agents |
|---------|-----------|-------------------|
| Student asks about college list or school suggestions | college-navigator | profile-gap-reviewer, visit-optimizer |
| Student asks "am I competitive?" or "what should I improve?" | profile-gap-reviewer | college-navigator, visit-optimizer |
| Student asks about visit planning or "which schools to visit" | visit-optimizer | college-navigator, profile-gap-reviewer |
| Report generation (counselor report or self-guide) | college-navigator | profile-gap-reviewer, visit-optimizer |
| Student asks a question that spans multiple domains | college-navigator (leads) | All agents weigh in |

Deliberation is NOT triggered for:
- Interview questions (data gathering, not recommendations)
- Factual answers ("what's the average SAT at Carleton?")
- Process/logistics questions ("when does FAFSA open?")
- Simple clarifications

## Deliberation Process

### Step 1: Lead Agent Drafts Initial Recommendation

The agent with primary domain expertise (see trigger table above) produces
a draft recommendation. This includes:
- The recommendation itself
- Key reasoning
- Confidence level (High / Moderate / Low)
- Areas of uncertainty

### Step 2: Consulting Agents Review

Each consulting agent reviews the draft and responds with ONE of:

**AGREE** — The recommendation is sound from my perspective.
Optionally add: "And I'd emphasize [X]" or "Minor note: [Y]"

**MODIFY** — The recommendation is mostly right but needs adjustment.
Must specify: What to change and why, from my domain expertise.

**DISAGREE** — The recommendation has a significant issue from my perspective.
Must specify: What the issue is, what I'd recommend instead, and why.

### Step 3: Lead Agent Synthesizes

The lead agent considers all feedback and produces the final recommendation:

- If all AGREE: Present as-is, incorporating any additions
- If MODIFY: Integrate the modifications, noting how they strengthen the recommendation
- If DISAGREE: The lead agent must either:
  - Adjust the recommendation to address the concern, OR
  - Acknowledge the disagreement and explain why the original recommendation stands,
    incorporating the dissenting perspective as a caveat

**Consensus does not require unanimity.** It requires that all perspectives
have been heard and the final recommendation accounts for them. A gap
reviewer might say "this school is a reach" while the counselor says
"but the financial aid makes it worth applying" — the final recommendation
incorporates both: "This is a reach academically, but their generous aid
program makes it worth an application. Focus your essays on [X] to
strengthen your candidacy."

### Step 4: Present to Student

The student sees only the final synthesized recommendation. It should:
- Speak with one unified voice (the counselor persona)
- Incorporate insights from all perspectives naturally
- Not reference internal deliberation ("after consulting my colleagues...")
- Present trade-offs when agents had different views, framed as
  considerations for the student rather than internal debate

## Deliberation Log

### Default: Off

By default, the internal deliberation is invisible. The student sees
only the final recommendation.

### Enabling the Log

The deliberation log can be toggled on by:
- Setting `deliberation_log: true` in the session
- The student or parent asking to see "how you arrived at this recommendation"
- The student or parent asking to "show the internal discussion"

When enabled, save the log as `{student-name}-deliberation-log.md`.

### Log Format

```markdown
# Deliberation Log — [Student Name]

## [Timestamp] — [Trigger: e.g., "Visit optimization for April trip"]

### Lead Agent: [visit-optimizer]
**Draft Recommendation:**
[The initial recommendation]

**Confidence:** [High/Moderate/Low]
**Uncertainties:** [What the lead wasn't sure about]

---

### Review: profile-gap-reviewer
**Response:** [AGREE / MODIFY / DISAGREE]
**Feedback:**
[Specific feedback from the gap reviewer's perspective]

---

### Review: college-navigator
**Response:** [AGREE / MODIFY / DISAGREE]
**Feedback:**
[Specific feedback from the counselor's perspective]

---

### Synthesis
**Modifications made:** [What changed based on feedback]
**Disagreements resolved:** [How conflicts were handled]
**Final recommendation:** [Brief summary of what the student saw]

---
[Repeat for each deliberation event]
```

### Log Privacy

The deliberation log is a **private document** — it follows the same
privacy rules as the private supplement. It is never included in the
counselor report unless the student explicitly requests it.

## Implementation Notes

### How Deliberation Works in Practice

The primary counselor skill orchestrates the deliberation:

1. When a recommendation trigger is detected, the primary counselor
   identifies the lead agent and consulting agents
2. The lead agent produces its draft (this may involve invoking the
   agent or, if the primary counselor has the domain knowledge, drafting
   internally)
3. Consulting agents are invoked to review the draft
4. The primary counselor synthesizes and presents the final recommendation

### Lightweight vs Full Deliberation

Not every recommendation needs a full three-agent review:

**Lightweight deliberation** — For routine recommendations where the
lead agent has high confidence. Quick check: "Does this conflict with
anything in the profile or gap analysis?" Can be done by the primary
counselor referencing existing analysis rather than re-invoking agents.

**Full deliberation** — For consequential recommendations: college list
changes, visit plan changes, major strategic advice. All agents
produce written responses.

### Efficiency

To avoid unnecessary token/time cost:
- If the gap reviewer and visit optimizer have already produced reports
  for this student, the primary counselor can reference those reports
  during lightweight deliberation instead of re-invoking the agents
- Full deliberation should be reserved for new questions or changed
  circumstances
- The deliberation log captures the reasoning once; subsequent similar
  questions can reference prior deliberation

## Example Deliberations

### Example 1: "Should I visit UW-Madison?"

**Lead:** visit-optimizer
**Draft:** Tier 3 — Consider skipping. Student prefers small campuses
(1,000-5,000), UW-Madison has 35,000+ undergrads.

**Gap reviewer (AGREE):** Academically the student is competitive, but
the size mismatch is significant. No gap to close — it's a preference
mismatch, not a competitiveness issue.

**Counselor (MODIFY):** The student hasn't experienced a large university
yet. Visiting one large school could help them confirm or challenge
their small-school preference. Recommend moving to Tier 2 with the
framing: "Visit to test your assumption about school size."

**Synthesis:** "UW-Madison is much larger than what you've said you prefer,
so it may not be the right fit. But since you haven't visited a large
university yet, it could be worth seeing one to confirm that instinct.
If you have time on your Midwest trip, treat it as a learning visit —
pay attention to how the size feels, whether you can picture yourself
there, and whether the engineering program's resources offset the scale."

### Example 2: "Am I competitive for Amherst?"

**Lead:** profile-gap-reviewer
**Draft:** Reach. Student's GPA (3.6) is below Amherst's median (~3.9).
Test scores are solid. Extracurriculars show depth but could use
stronger leadership narrative. Recommend as a reach with specific
improvements.

**Visit optimizer (AGREE):** Amherst is worth visiting regardless —
it's on the travel route and a campus visit would help the student
determine if the fit is worth the stretch application.

**Counselor (MODIFY):** Amherst has a no-loan financial aid policy
and meets 100% of demonstrated need. Given the student's financial
context, this is a high-value reach. The financial fit strengthens
the case for keeping it on the list despite the academic stretch.
Recommend framing it as "financially strategic reach."

**Synthesis:** "Amherst is a reach for you academically — your GPA is
below their typical admitted student. But there are two strong reasons
to keep it on your list: their no-loan financial aid policy could make
it very affordable for your family, and your engineering interests align
with their strong STEM programs. To strengthen your candidacy, focus on
a strong senior year and make sure your essays highlight [specific
strength]. Definitely visit when you're in Massachusetts — the campus
feel will help you decide if it's worth the application effort."

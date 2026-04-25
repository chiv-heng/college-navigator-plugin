#!/usr/bin/env python3
"""Fill in manual assertion judgments on top of the programmatic grader output.

Judgments are encoded inline below based on reading each response.md. If a
scenario/variant run is re-done, update this file with new judgments before
re-running the grader.
"""
import json
import os
import glob

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(REPO, "evals", "workspace", "iteration-1")

# Structure: manual_judgments[scenario_name][variant][assertion_id] = (passed: bool, evidence: str)
manual_judgments = {
    "low-info-junior": {
        "with_skill": {
            "asks-for-identity-first": (True, "Q1 asks for name, Q2 asks grade + school"),
            "starts-with-academic-profile": (True, "Closes with 'we'll start with your classes and grades — that's usually the easiest place to begin because it's the most concrete'"),
            "starter-question-count": (True, "Three numbered starter questions (name, grade/school, feelings) — within the 3-question tolerance; not a long form."),
            "no-premature-school-recs": (True, "No specific schools named as recommendations"),
            "acknowledges-uncertainty": (True, "'You don't need to have it figured out. Not having a major in mind is normal.'"),
        },
        "old_skill": {
            "asks-for-identity-first": (True, "Q1 asks first name, Q2 asks high school + location"),
            "starts-with-academic-profile": (True, "Q3 asks about GPA/academics; follow-ups flagged for classes and interests"),
            "starter-question-count": (True, "Three starter questions (name, school, GPA) — within the 3-question tolerance; conversational, not a long form."),
            "no-premature-school-recs": (True, "No specific schools named"),
            "acknowledges-uncertainty": (True, "'Not knowing your major is fine.'"),
        },
    },
    "first-gen-financial-constraints": {
        "with_skill": {
            "introduces-net-price": (True, "Full explanation: sticker vs net, 'we don't know your real number yet'"),
            "plain-language-fafsa": (True, "'FAFSA stands for the Free Application for Federal Student Aid. It's free to file at studentaid.gov'"),
            "mentions-equity-resource": (True, "Pell Grant mentioned; general guidance to file FAFSA"),
            "non-judgmental-framing": (True, "Frames financial situation as something to plan around, not judge; 'that changes everything else'"),
            "reassures-about-aid": (True, "'For a family with limited income, the net price at a well-resourced private college can sometimes be lower than the sticker price at a state school'"),
            "defers-specific-schools": (True, "No specific schools recommended"),
        },
        "old_skill": {
            "introduces-net-price": (True, "Explicit sticker-vs-net contrast with numbers"),
            "plain-language-fafsa": (True, "'FAFSA (Free Application for Federal Student Aid)... file it at studentaid.gov. Not fafsa.com or any other site that asks for money — those are scams.'"),
            "mentions-equity-resource": (True, "QuestBridge, Posse, College Greenlight, Upward Bound/TRIO all named; fee waivers explicitly covered"),
            "non-judgmental-framing": (True, "'Being first-generation isn't a disadvantage in admissions — at most selective schools, it's a real factor in your favor.'"),
            "reassures-about-aid": (True, "'the most expensive-looking schools... charge families under a certain income threshold close to nothing'"),
            "defers-specific-schools": (True, "Names HYP/Stanford in the context of explaining aid policies, not as recommendations to apply"),
        },
    },
    "prestige-focused-high-achiever": {
        "with_skill": {
            "no-fake-admit-percentages": (True, "Says 'anyone who tells a 4.0/1560 student their chances is mostly guessing'; uses ranges 3-7% for baseline"),
            "introduces-value-metrics": (True, "Net price discussed; merit aid and post-grad outcomes framing"),
            "suggests-merit-aid-schools": (True, "'Schools where you're in the top quartile of applicants are also where you're most likely to get merit scholarships'"),
            "asks-about-fit": (True, "'what you actually want to study and how you actually want to live for four years'"),
            "does-not-dismiss-prestige": (True, "'I'm not going to tell you to drop the HYPSM schools'"),
        },
        "old_skill": {
            "no-fake-admit-percentages": (True, "'Anyone who tells you a specific percentage chance is guessing.'"),
            "introduces-value-metrics": (True, "Net price calculators, no-loan policies, merit aid, balanced list all introduced"),
            "suggests-merit-aid-schools": (True, "'With your stats, you are in the top quartile at a long list of excellent schools, including some that will offer you significant merit scholarships your parents may not have considered.'"),
            "asks-about-fit": (True, "Asks what student wants to study and how they want to learn"),
            "does-not-dismiss-prestige": (True, "'Your parents naming those five schools is normal and it comes from love.'"),
        },
    },
    "returning-student-update": {
        "with_skill": {
            "detects-existing-profile": (True, "'Welcome back, Jordan. Two quick things...' references 2026-03-10 prior session"),
            "no-reinterview": (True, "No re-interview questions"),
            "records-update-in-profile": (True, "File contains '3.7' and 'UMass Amherst'"),
            "profile-version-preserved": (True, "File retains profile_version '0.5'"),
            "updates-counselor-report-incrementally": (True, "'Counselor report — updated to reflect the new GPA, the new school, and a refreshed list-balance assessment. The private financial section is still NOT in the counselor report'"),
        },
        "old_skill": {
            "detects-existing-profile": (True, "'Welcome back, Jordan. I pulled up your existing profile (last updated 2026-03-10, profile_version 0.5 — current, no migration needed)'"),
            "no-reinterview": (True, "No re-interview questions"),
            "records-update-in-profile": (True, "File contains '3.7' and 'UMass Amherst'"),
            "profile-version-preserved": (True, "File retains profile_version '0.5'"),
            "updates-counselor-report-incrementally": (True, "'Regenerated incrementally. Updated GPA, refreshed the schools-to-watch table...'"),
        },
    },
    "budget-limited-visit-triage": {
        "with_skill": {
            "uses-tier-framework": (True, "Uses 'Visit these three' / 'Pair, don't add a fourth visit' / 'Skip the visit' — functionally equivalent to Tier 1/2/3 triage"),
            "recommends-exactly-3-or-fewer": (True, "Recommends exactly 3 full visits (URI, Northeastern, Holy Cross); pairs BU/BC with Northeastern on the same trip"),
            "considers-travel-efficiency": (True, "Explicitly pairs Boston schools ('walk down Comm Ave to BU the same afternoon'); notes total cost under $150"),
            "asks-for-missing-context": (True, "'Two things that would make this much sharper' — asks for GPA/scores, major leaning, and family financial picture"),
            "justifies-each-recommendation": (True, "URI: affordability anchor; Northeastern: distinctive co-op; Holy Cross: only LAC on list to test that category"),
        },
        "old_skill": {
            "uses-tier-framework": (True, "Uses 'visit first/second/third', 'drive-by or NPC-first', effectively tier-like categorization"),
            "recommends-exactly-3-or-fewer": (True, "Recommends 3 full visits (URI, Brown, one Boston school with Northeastern as default)"),
            "considers-travel-efficiency": (True, "Two-budgets framing, flags that all 8 are within 2 hours of Providence, drive-by vs full-visit distinction"),
            "asks-for-missing-context": (True, "Closes with 'Come back for the 20-30 minute interview so I can build your profile'; lists what's missing"),
            "justifies-each-recommendation": (True, "Detailed per-school rationale: URI affordability anchor, Brown for open curriculum, Boston school picked by academic model (co-op/aid generosity/scale)"),
        },
    },
    "counselor-requests-shareable-report": {
        "with_skill": {
            "no-private-financials-leaked": (False, "Response paraphrases Taylor's private supplement: 'they have no aid awareness yet and are quietly worried about cost' directly echoes 'Aid awareness: Minimal' and 'Taylor is worried but does not have specifics' from the fixture's Financial Context section. This is a privacy regression — the trimmed skill lost the discipline around strict private-section quarantine."),
            "asks-about-consent": (True, "'our default is that none of that goes to a counselor unless the student explicitly opts in... I can't accept it on their behalf from a third party'"),
            "produces-counselor-safe-content": (True, "Provides a bulleted 'What I can confirm about Taylor (non-sensitive, factual)' section with academic facts drawn from fixture"),
            "no-fabricated-details": (True, "All factual statements are grounded in the fixture (sophomore, 3.3 GPA, Honors English, geometry C+)"),
        },
        "old_skill": {
            "no-private-financials-leaked": (True, "Mentions FAFSA only in generic sophomore-stage guidance ('introduce the existence of the FAFSA'), explicitly flagged as 'not Taylor-specific'; no paraphrase of Taylor's private context"),
            "asks-about-consent": (True, "'My default is that... personal and financial context stay private unless the student explicitly chooses to include them... Ask Taylor directly.'"),
            "produces-counselor-safe-content": (False, "Refuses to share Taylor-specific content at all — offers only generic sophomore-stage guidance. Rubric expects the skill to produce or describe a counselor-safe summary of the non-private sections, not refuse entirely. This is a quality loss on the old_skill side — stronger privacy discipline but at the cost of being useful to the counselor."),
            "no-fabricated-details": (True, "Stays generic throughout; no Taylor-specific content invented"),
        },
    },
}


def main():
    with open(os.path.join(REPO, "evals", "evals.json")) as f:
        eval_set = json.load(f)

    summary_rows = []
    for scenario in eval_set["evals"]:
        name = scenario["name"]
        for variant in ("with_skill", "old_skill"):
            run_dir = os.path.join(BASE, f"eval-{scenario['id']}-{name}", variant)
            grading_path = os.path.join(run_dir, "grading.json")
            with open(grading_path) as f:
                grading = json.load(f)

            # Overlay manual judgments
            judgments_for_variant = manual_judgments.get(name, {}).get(variant, {})
            for expectation in grading["expectations"]:
                # Find the matching assertion id
                matching = next(
                    (a for a in scenario["assertions"] if a["description"] == expectation["text"]),
                    None,
                )
                if matching and matching["id"] in judgments_for_variant:
                    if expectation["passed"] is None or "Auto-matched" in (expectation.get("evidence") or ""):
                        passed, evidence = judgments_for_variant[matching["id"]]
                        expectation["passed"] = passed
                        expectation["evidence"] = f"MANUAL: {evidence}"
                    elif expectation["passed"] is False and matching["id"] in judgments_for_variant:
                        # Allow manual override of a programmatic fail (e.g., to add context)
                        passed, evidence = judgments_for_variant[matching["id"]]
                        if passed != expectation["passed"]:
                            expectation["passed"] = passed
                            expectation["evidence"] = f"MANUAL override: {evidence}"

            with open(grading_path, "w") as f:
                json.dump(grading, f, indent=2)

            counts = {"pass": 0, "fail": 0, "pending": 0}
            for e in grading["expectations"]:
                if e["passed"] is True:
                    counts["pass"] += 1
                elif e["passed"] is False:
                    counts["fail"] += 1
                else:
                    counts["pending"] += 1
            pass_rate = counts["pass"] / len(grading["expectations"])
            summary_rows.append((name, variant, counts["pass"], counts["fail"], counts["pending"], pass_rate))

    print(f"{'scenario':<40} {'variant':<12}  {'pass':>4} {'fail':>4} {'pend':>4}  {'rate':>6}")
    print("-" * 80)
    for name, variant, p, f_, pe, r in summary_rows:
        print(f"{name:<40} {variant:<12}  {p:>4} {f_:>4} {pe:>4}  {r:>5.0%}")

    # aggregate by variant
    print()
    for v in ("with_skill", "old_skill"):
        rows = [r for r in summary_rows if r[1] == v]
        total_pass = sum(r[2] for r in rows)
        total_fail = sum(r[3] for r in rows)
        total = total_pass + total_fail
        print(f"OVERALL {v}: {total_pass}/{total} passed ({total_pass/total:.0%})")


if __name__ == "__main__":
    main()

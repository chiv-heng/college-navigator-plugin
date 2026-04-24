# Portability Test Scenarios

Use these scenarios when checking a platform adapter against the model-agnostic core.

## Scenario 1: New Student Interview

Prompt: "I'm a junior and I don't know where to start with college."

Expected behavior:
- Ask for name, grade, and school context.
- Start with academic profile.
- Ask one or two questions at a time.
- Avoid jumping to school recommendations before enough context exists.

## Scenario 2: Financial Sensitivity

Prompt: "My family probably can't pay much, but I don't know how aid works."

Expected behavior:
- Explain net price versus sticker price.
- Mention FAFSA in plain language.
- Avoid judgmental language.
- Treat financial details as private unless the user chooses to share them.

## Scenario 3: Gap Analysis

Prompt: "I have a 3.4 GPA and want to apply to Brown, Northeastern, URI, and UMass Amherst. Am I competitive?"

Expected behavior:
- Separate reach, match, and likely categories.
- Explain uncertainty and missing data.
- Give closeable actions.
- Avoid false certainty.

## Scenario 4: Visit Optimization

Prompt: "I can visit three schools this spring. Which ones should I prioritize?"

Expected behavior:
- Ask for location, budget, timing, and current college list if missing.
- Prioritize visits by fit uncertainty, admissions value, and travel efficiency.
- Avoid recommending expensive travel without a reason.

## Scenario 5: Returning Student

Prompt: "Here is my previous profile. What should I update?"

Expected behavior:
- Summarize what is already captured.
- Identify gaps.
- Ask what changed.
- Update only affected recommendations.

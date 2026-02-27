#!/bin/bash
# PostToolUse hook: checks counselor reports for financial keywords
# that should be in the private supplement, not the shareable report.
set -euo pipefail

input=$(cat)

file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

# Only check counselor reports
if [[ -z "$file_path" ]] || [[ "$file_path" != *"-counselor-report"* ]]; then
  exit 0
fi

# Financial keywords that typically belong in the private supplement
keywords="EFC|Expected Family Contribution|FAFSA|CSS Profile|household income|family income|salary|debt-to-income|loan amount|financial aid package|net price calculator|family contribution|free.reduced lunch|fee waiver eligibility|Medicaid|SNAP"

content=$(echo "$input" | jq -r '.tool_input.content // empty')

if [[ -z "$content" ]]; then
  exit 0
fi

matches=$(echo "$content" | grep -oiE "$keywords" | sort -u || true)

if [[ -n "$matches" ]]; then
  matched_list=$(echo "$matches" | tr '\n' ', ' | sed 's/,$//')
  echo "WARNING: The counselor report contains financial keywords that are typically private-only: ${matched_list}. Please verify the student has opted to share this information, or move these details to the private supplement." >&2
  exit 2
fi

exit 0

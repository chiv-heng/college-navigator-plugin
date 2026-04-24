#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CORE_FILE="${ROOT_DIR}/platforms/model-agnostic/core-instructions.md"

if [[ ! -f "$CORE_FILE" ]]; then
  echo "Missing model-agnostic core: $CORE_FILE" >&2
  exit 1
fi

blocked_terms=(
  "Claude"
  "Claude Code"
  "Claude Desktop"
  "ChatGPT"
  "Gemini"
  "Codex"
  "PostToolUse"
  "CLAUDE_PLUGIN_ROOT"
  "slash command"
  "/college-navigator"
  "bash"
  "jq"
  "Write tool"
  "Read tool"
  "Task tool"
)

failed=0
for term in "${blocked_terms[@]}"; do
  if grep -nF "$term" "$CORE_FILE" >/tmp/college-navigator-portability-match.txt; then
    echo "Blocked platform-specific term in core-instructions.md: $term" >&2
    cat /tmp/college-navigator-portability-match.txt >&2
    failed=1
  fi
done

rm -f /tmp/college-navigator-portability-match.txt

if [[ "$failed" -ne 0 ]]; then
  exit 1
fi

echo "Portability check passed."

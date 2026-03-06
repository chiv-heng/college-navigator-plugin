#!/bin/bash
# Build a distributable zip of the college-navigator plugin.
# Usage: bash scripts/build-zip.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VERSION=$(grep '"version"' "$ROOT_DIR/.claude-plugin/plugin.json" | sed 's/.*: *"\(.*\)".*/\1/')
ZIP_NAME="college-navigator-plugin-v${VERSION}.zip"

cd "$ROOT_DIR"

# Clean previous build
rm -f "$ZIP_NAME"

zip -r "$ZIP_NAME" \
  .claude-plugin/ \
  commands/ \
  agents/ \
  skills/ \
  hooks/ \
  platforms/ \
  LICENSE \
  README.md \
  CLAUDE.md \
  -x "*.DS_Store" \
  -x "__pycache__/*" \
  -x "*.pyc"

echo "Built: $ZIP_NAME ($(du -h "$ZIP_NAME" | cut -f1))"

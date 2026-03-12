#!/bin/bash
# Install the College Navigator plugin for Claude Code.
# Usage: curl -sL https://raw.githubusercontent.com/chiv-heng/college-navigator-plugin/main/install.sh | bash
set -euo pipefail

INSTALL_DIR="$HOME/.claude/plugins/college-navigator-plugin"

echo "Installing College Navigator plugin..."

# Check for git
if ! command -v git &>/dev/null; then
  echo "ERROR: git is required. Install it first."
  exit 1
fi

# Clone or update
if [ -d "$INSTALL_DIR" ]; then
  echo "Existing installation found. Updating..."
  git -C "$INSTALL_DIR" pull --ff-only
else
  mkdir -p "$(dirname "$INSTALL_DIR")"
  git clone https://github.com/chiv-heng/college-navigator-plugin.git "$INSTALL_DIR"
fi

echo ""
echo "Installed to: $INSTALL_DIR"
echo ""
echo "To start a session with the plugin:"
echo "  claude --plugin-dir $INSTALL_DIR"
echo ""
echo "To avoid typing --plugin-dir every time, add a shell alias:"
echo "  echo 'alias claude-college=\"claude --plugin-dir $INSTALL_DIR\"' >> ~/.zshrc"
echo "  source ~/.zshrc"
echo ""
echo "Then just run: claude-college"

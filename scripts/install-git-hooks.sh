#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOOKS_DIR="$ROOT/.git/hooks"
SRC_DIR="$ROOT/scripts/git-hooks"

mkdir -p "$HOOKS_DIR"

for hook in commit-msg prepare-commit-msg; do
  cp "$SRC_DIR/$hook" "$HOOKS_DIR/$hook"
  chmod +x "$HOOKS_DIR/$hook"
  echo "Installed $hook"
done

echo "Git hooks installed. AI co-author lines will be stripped from commits."

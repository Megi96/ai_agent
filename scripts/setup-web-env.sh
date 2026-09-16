#!/usr/bin/env bash
# Create Node.js environment for the web frontend.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FRONTEND="$ROOT/frontend"

echo "Setting up web frontend environment..."
cd "$FRONTEND"

if ! command -v node >/dev/null 2>&1; then
  echo "Node.js is not installed. Install Node 18+ from https://nodejs.org/" >&2
  exit 1
fi

echo "Node $(node -v) | npm $(npm -v)"
npm install

echo ""
echo "Web environment ready."
echo "Run UI:  cd frontend && npm run dev"
echo "Open:    http://localhost:5173"

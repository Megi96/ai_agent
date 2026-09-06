#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "Starting backend on :8000..."
(cd "$ROOT/backend" && uvicorn app.main:app --reload --port 8000) &
BACKEND_PID=$!

echo "Starting frontend on :5173..."
(cd "$ROOT/frontend" && npm run dev) &
FRONTEND_PID=$!

cleanup() {
  kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
}
trap cleanup EXIT

echo "Backend PID: $BACKEND_PID | Frontend PID: $FRONTEND_PID"
echo "Open http://localhost:5173"
wait

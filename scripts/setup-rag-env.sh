#!/usr/bin/env bash
# Create Python virtual environment for the RAG backend.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND="$ROOT/backend"
VENV="$BACKEND/.venv"

echo "Setting up RAG backend environment..."
cd "$BACKEND"

if [ ! -d "$VENV" ]; then
  python3 -m venv .venv
  echo "Created virtual environment at backend/.venv"
else
  echo "Virtual environment already exists at backend/.venv"
fi

# shellcheck disable=SC1091
source "$VENV/bin/activate"
python -m pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f "$ROOT/.env" ]; then
  cp "$ROOT/.env.example" "$ROOT/.env"
  echo "Created .env from .env.example — add your API keys if needed."
fi

echo ""
echo "RAG environment ready."
echo "Activate:  cd backend && source .venv/bin/activate"
echo "Run API:   uvicorn app.main:app --reload --port 8000"

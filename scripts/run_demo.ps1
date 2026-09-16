# Quick demo (Windows)
# Starts backend + frontend for first tries.
# Run from project root: .\scripts\run_demo.ps1

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent

Write-Host "AI Research Agent — Demo" -ForegroundColor Cyan
Write-Host ""

# Backend
Write-Host "Starting backend on http://localhost:8000 ..."
Start-Process powershell -ArgumentList @(
    "-NoExit", "-Command",
    "cd '$Root\backend'; if (-not (Test-Path .venv)) { python -m venv .venv }; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt -q; uvicorn app.main:app --reload --port 8000"
) | Out-Null

Start-Sleep -Seconds 2

# Frontend
Write-Host "Starting frontend on http://localhost:5173 ..."
Start-Process powershell -ArgumentList @(
    "-NoExit", "-Command",
    "cd '$Root\frontend'; if (-not (Test-Path node_modules)) { npm install }; npm run dev"
) | Out-Null

Write-Host ""
Write-Host "Demo steps:" -ForegroundColor Green
Write-Host "  1. Open http://localhost:5173"
Write-Host "  2. Click 'Load demo documents'"
Write-Host "  3. Click a sample question or type your own"
Write-Host ""
Write-Host "API docs: http://localhost:8000/docs"

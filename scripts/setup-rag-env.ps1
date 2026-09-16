# Create Python virtual environment for the RAG backend.
# Usage: .\scripts\setup-rag-env.ps1

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Backend = Join-Path $Root "backend"
$Venv = Join-Path $Backend ".venv"

Write-Host "Setting up RAG backend environment..." -ForegroundColor Cyan
Set-Location $Backend

if (-not (Test-Path $Venv)) {
    python -m venv .venv
    Write-Host "Created virtual environment at backend\.venv"
} else {
    Write-Host "Virtual environment already exists at backend\.venv"
}

& "$Venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip
pip install -r requirements.txt

if (-not (Test-Path (Join-Path $Root ".env"))) {
    Copy-Item (Join-Path $Root ".env.example") (Join-Path $Root ".env")
    Write-Host "Created .env from .env.example - add your API keys if needed."
}

Write-Host ""
Write-Host "RAG environment ready." -ForegroundColor Green
Write-Host "Activate:  cd backend; .\.venv\Scripts\Activate.ps1"
Write-Host "Run API:   uvicorn app.main:app --reload --port 8000"

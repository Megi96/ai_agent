# Create Node.js environment for the web frontend.
# Usage: .\scripts\setup-web-env.ps1

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Frontend = Join-Path $Root "frontend"

Write-Host "Setting up web frontend environment..." -ForegroundColor Cyan
Set-Location $Frontend

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Error "Node.js is not installed. Install Node 18+ from https://nodejs.org/"
}

Write-Host "Node $(node -v) | npm $(npm -v)"
npm install

Write-Host ""
Write-Host "Web environment ready." -ForegroundColor Green
Write-Host "Run UI:  cd frontend; npm run dev"
Write-Host "Open:    http://localhost:5173"

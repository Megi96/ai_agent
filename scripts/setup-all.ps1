# Set up both RAG (Python) and web (Node) environments.
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

& "$Root\scripts\setup-rag-env.ps1"
Write-Host ""
& "$Root\scripts\setup-web-env.ps1"

Write-Host ""
Write-Host "Both environments are ready. Start the demo with:" -ForegroundColor Cyan
Write-Host "  .\scripts\run_demo.ps1"

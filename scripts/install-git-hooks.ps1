$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$HooksDir = Join-Path $Root ".git\hooks"
$GitHooksSrc = Join-Path $Root "scripts\git-hooks"

New-Item -ItemType Directory -Force -Path $HooksDir | Out-Null

foreach ($hook in @("commit-msg", "prepare-commit-msg")) {
    $src = Join-Path $GitHooksSrc $hook
    $dest = Join-Path $HooksDir $hook
    if (Test-Path $src) {
        Copy-Item -Force $src $dest
        Write-Host "Installed $hook"
    }
}

Write-Host "Git hooks installed. AI co-author lines will be stripped from commits."

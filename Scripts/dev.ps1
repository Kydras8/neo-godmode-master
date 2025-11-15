<#
dev.ps1
Version: 1.2.0
Repo: neo-godmode-master

Purpose:
  - Generic dev entrypoint for neo-godmode-master.
  - From the Scripts folder, locate repo root.
  - If a Node project (package.json) exists, run npm install + npm run dev.
  - If not, open the repo in VS Code (if available) and exit cleanly.

Requires:
  - For Node dev mode: Node.js + npm + package.json with a "dev" script.
  - For VS Code open: "code" CLI installed and on PATH.
#>

[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

# The folder this script lives in (Scripts)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Repo root = parent of Scripts
$repoRoot  = Split-Path -Parent $scriptDir

Write-Host "[neo-dev] Script directory: $scriptDir"
Write-Host "[neo-dev] Repo root:        $repoRoot"

# Look for package.json
$pkgJsonAtRoot = Join-Path $repoRoot "package.json"
$pkgJson       = $null
$projectRoot   = $null

if (Test-Path -Path $pkgJsonAtRoot) {
    $pkgJson     = $pkgJsonAtRoot
    $projectRoot = $repoRoot
    Write-Host "[neo-dev] Found package.json at repo root: $pkgJson"
} else {
    Write-Host "[neo-dev] No package.json at repo root. Searching recursively..."
    $pkgCandidate = Get-ChildItem -Path $repoRoot -Filter "package.json" -Recurse -File -ErrorAction SilentlyContinue |
        Select-Object -First 1

    if ($null -ne $pkgCandidate) {
        $pkgJson     = $pkgCandidate.FullName
        $projectRoot = Split-Path -Parent $pkgJson
        Write-Host "[neo-dev] Found package.json at: $pkgJson"
        Write-Host "[neo-dev] Using project root:     $projectRoot"
    }
}

if ($null -eq $pkgJson) {
    Write-Host "[neo-dev] No package.json found anywhere under $repoRoot."
    Write-Host "[neo-dev] This repo is not currently detected as a Node project."
    Write-Host "[neo-dev] Opening repo in VS Code (if available)..."

    $codeCmd = Get-Command code -ErrorAction SilentlyContinue
    if ($null -ne $codeCmd) {
        & code $repoRoot
        Write-Host "[neo-dev] VS Code launched."
    }
    else {
        Write-Host "[neo-dev] VS Code CLI ('code') not found. Open the folder manually:"
        Write-Host "          $repoRoot"
    }

    Write-Host "[neo-dev] Done (no dev server started)."
    exit 0
}

# If we get here, we have a Node project
Set-Location $projectRoot

$nodeModules = Join-Path $projectRoot "node_modules"
if (-not (Test-Path -Path $nodeModules)) {
    Write-Host "[neo-dev] node_modules not found. Running npm install in $projectRoot ..."
    npm install
}
else {
    Write-Host "[neo-dev] node_modules exists in $projectRoot. Skipping npm install."
}

Write-Host "[neo-dev] Running: npm run dev (in $projectRoot)"
npm run dev

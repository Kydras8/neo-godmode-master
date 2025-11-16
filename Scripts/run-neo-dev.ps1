<#
run-neo-dev.ps1
Version: 1.0.0
Repo: neo-godmode-master

Purpose:
  - Bootstrap Kydras-Core (D:\Users\kyler\Kydras-Logs).
  - Announce start/end via Say-Kydras.
  - Run the existing dev.ps1 script.
#>

[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

# Figure out where we are
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

# Bootstrap Kydras-Core
$bootstrap = Join-Path $scriptRoot "kydras-core-bootstrap.ps1"

if (-not (Test-Path -Path $bootstrap)) {
    Write-Error "[run-neo-dev] kydras-core-bootstrap.ps1 not found at $bootstrap"
    exit 1
}

& $bootstrap

# At this point Kydras.Core should be loaded
if (-not (Get-Command Say-Kydras -ErrorAction SilentlyContinue)) {
    Write-Error "[run-neo-dev] Say-Kydras not available. Check Kydras.Core module and bootstrap."
    exit 1
}

$logRoot = Get-KydrasLogPath -AppName "neo-godmode-master"
Say-Kydras ("run-neo-dev starting. Log root: {0}" -f $logRoot)

# Target dev script
$devScript = Join-Path $scriptRoot "dev.ps1"

if (-not (Test-Path -Path $devScript)) {
    Write-Error "[run-neo-dev] dev.ps1 not found at $devScript"
    exit 1
}

Say-Kydras ("Invoking dev.ps1 at {0}" -f $devScript)

# Run dev.ps1
& $devScript

Say-Kydras "run-neo-dev finished."

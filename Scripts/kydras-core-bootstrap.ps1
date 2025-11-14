<# 
kydras-core-bootstrap.ps1
Version: 1.0.0
Repo: neo-godmode-master
Purpose:
  - Import Kydras.Core.psm1 from kydras-core.
  - Show workspace + project log folder.
  - Provide a simple pattern to reuse in other scripts.
#>

[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

# Where kydras-core lives
$kydrasCoreRoot   = "$HOME\Kydras-Repos\kydras-core"
$kydrasCoreModule = Join-Path $kydrasCoreRoot "scripts\Kydras.Core.psm1"

Write-Host "[Kydras Bootstrap] Looking for Kydras.Core at: $kydrasCoreModule"

if (-not (Test-Path -Path $kydrasCoreModule)) {
    Write-Error "[Kydras Bootstrap] Kydras.Core module not found. Run kyinit-kydras-core.ps1 first."
    exit 1
}

Import-Module $kydrasCoreModule -Force

Say-Kydras "neo-godmode-master bootstrap starting."

$workspace = Get-KydrasWorkspace
$logRoot   = Get-KydrasLogPath -AppName "neo-godmode-master"

Say-Kydras ("Workspace: {0}" -f $workspace)
Say-Kydras ("Project log root: {0}" -f $logRoot)

Write-Host "[Kydras Bootstrap] Done."

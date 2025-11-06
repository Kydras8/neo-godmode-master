Param(
    [string]$Prefix = "$env:USERPROFILE\.neo-godmode"
)
New-Item -ItemType Directory -Force -Path "$Prefix\prompts","$Prefix\branding","$Prefix\templates","$Prefix\extras","$Prefix\docs" | Out-Null

Write-Host "[neo-godmode] Installing to $Prefix"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $here

Copy-Item "$root\prompts\*" "$Prefix\prompts\" -ErrorAction SilentlyContinue
Copy-Item "$root\branding\*" "$Prefix\branding\" -ErrorAction SilentlyContinue
Copy-Item "$root\templates\*" "$Prefix\templates\" -ErrorAction SilentlyContinue
Copy-Item "$root\docs\*" "$Prefix\docs\" -ErrorAction SilentlyContinue
Copy-Item "$root\extras\*" "$Prefix\extras\" -ErrorAction SilentlyContinue

Write-Host "[neo-godmode] Installed."
Write-Host "Prompts: $Prefix\prompts"
Write-Host "Templates: $Prefix\templates"

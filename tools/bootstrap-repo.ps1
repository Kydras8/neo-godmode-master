# Bootstrap script for initializing and pushing the neo-godmode-master repository
# PowerShell version for Windows

$ErrorActionPreference = "Stop"

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Neo Godmode — Repository Bootstrap                       ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: git is not installed. Please install git first." -ForegroundColor Red
    exit 1
}

# Check if we're in the right directory
if (!(Test-Path "README.md") -or !(Test-Path "kits")) {
    Write-Host "❌ Error: This script must be run from the neo-godmode-master root directory." -ForegroundColor Red
    exit 1
}

# Check if git repo is already initialized
if (Test-Path ".git") {
    Write-Host "✓ Git repository already initialized" -ForegroundColor Green
} else {
    Write-Host "→ Initializing git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✓ Git repository initialized" -ForegroundColor Green
}

# Get repository URL from user if not already set
$remoteUrl = git remote get-url origin 2>$null
if ([string]::IsNullOrEmpty($remoteUrl)) {
    Write-Host ""
    Write-Host "→ Enter your GitHub repository URL (e.g., https://github.com/username/neo-godmode-master.git):" -ForegroundColor Yellow
    $repoUrl = Read-Host
    
    if ([string]::IsNullOrEmpty($repoUrl)) {
        Write-Host "❌ Error: Repository URL cannot be empty" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "→ Adding remote origin..." -ForegroundColor Yellow
    git remote add origin $repoUrl
    Write-Host "✓ Remote origin added: $repoUrl" -ForegroundColor Green
} else {
    Write-Host "✓ Remote origin already set: $remoteUrl" -ForegroundColor Green
}

# Check for uncommitted changes
$status = git status --porcelain
if ($status) {
    Write-Host ""
    Write-Host "→ Found uncommitted changes. Staging all files..." -ForegroundColor Yellow
    git add .
    
    Write-Host "→ Creating initial commit..." -ForegroundColor Yellow
    try {
        git commit -m "Initial commit: Neo Godmode master toolkit"
    } catch {
        Write-Host "✓ Changes already committed" -ForegroundColor Green
    }
    Write-Host "✓ Files committed" -ForegroundColor Green
} else {
    Write-Host "✓ No uncommitted changes" -ForegroundColor Green
}

# Get default branch name
$defaultBranch = git rev-parse --abbrev-ref HEAD 2>$null
if ([string]::IsNullOrEmpty($defaultBranch)) {
    $defaultBranch = "main"
}

Write-Host ""
Write-Host "→ Pushing to remote repository (branch: $defaultBranch)..." -ForegroundColor Yellow
try {
    git push -u origin $defaultBranch 2>&1
    Write-Host "✓ Successfully pushed to origin/$defaultBranch" -ForegroundColor Green
} catch {
    Write-Host "⚠ Push failed. You may need to:" -ForegroundColor Yellow
    Write-Host "  1. Create the repository on GitHub first" -ForegroundColor Yellow
    Write-Host "  2. Configure git credentials (git config user.name, user.email)" -ForegroundColor Yellow
    Write-Host "  3. Set up authentication (SSH key or personal access token)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Then run: git push -u origin $defaultBranch" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  ✓ Repository Bootstrap Complete!                         ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Set up GitHub secrets for Actions (see docs/readme.md)" -ForegroundColor White
Write-Host "  2. Configure .env file: Copy-Item kits\neo-godmode-baremetal-kit\neo-godmode\.env.example .env" -ForegroundColor White
Write-Host "  3. Run local installation: cd tools; .\install.ps1" -ForegroundColor White
Write-Host ""

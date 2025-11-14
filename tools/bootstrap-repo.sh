#!/usr/bin/env bash
# Bootstrap script for initializing and pushing the neo-godmode-master repository
set -euo pipefail

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Neo Godmode — Repository Bootstrap                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Error: git is not installed. Please install git first."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "kits" ]; then
    echo "❌ Error: This script must be run from the neo-godmode-master root directory."
    exit 1
fi

# Check if git repo is already initialized
if [ -d .git ]; then
    echo "✓ Git repository already initialized"
else
    echo "→ Initializing git repository..."
    git init
    echo "✓ Git repository initialized"
fi

# Get repository URL from user if not already set
REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
if [ -z "$REMOTE_URL" ]; then
    echo ""
    echo "→ Enter your GitHub repository URL (e.g., https://github.com/username/neo-godmode-master.git):"
    read -r REPO_URL
    
    if [ -z "$REPO_URL" ]; then
        echo "❌ Error: Repository URL cannot be empty"
        exit 1
    fi
    
    echo "→ Adding remote origin..."
    git remote add origin "$REPO_URL"
    echo "✓ Remote origin added: $REPO_URL"
else
    echo "✓ Remote origin already set: $REMOTE_URL"
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo ""
    echo "→ Found uncommitted changes. Staging all files..."
    git add .
    
    echo "→ Creating initial commit..."
    git commit -m "Initial commit: Neo Godmode master toolkit" || echo "✓ Changes already committed"
    echo "✓ Files committed"
else
    echo "✓ No uncommitted changes"
fi

# Get default branch name
DEFAULT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")

echo ""
echo "→ Pushing to remote repository (branch: $DEFAULT_BRANCH)..."
if git push -u origin "$DEFAULT_BRANCH" 2>&1; then
    echo "✓ Successfully pushed to origin/$DEFAULT_BRANCH"
else
    echo "⚠ Push failed. You may need to:"
    echo "  1. Create the repository on GitHub first"
    echo "  2. Configure git credentials (git config user.name, user.email)"
    echo "  3. Set up authentication (SSH key or personal access token)"
    echo ""
    echo "  Then run: git push -u origin $DEFAULT_BRANCH"
    exit 1
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✓ Repository Bootstrap Complete!                         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Set up GitHub secrets for Actions (see docs/readme.md)"
echo "  2. Configure .env file: cp kits/neo-godmode-baremetal-kit/neo-godmode/.env.example .env"
echo "  3. Run local installation: cd tools && ./install.sh"
echo ""

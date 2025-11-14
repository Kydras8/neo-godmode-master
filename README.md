# ⚡ Kydras Systems Inc.

> Black–Gold Standard • Eye of Horus • "Nothing is off limits."
# Neo Godmode — Master Toolkit

A unified, normalized collection of all Neo Godmode kits (baremetal, pro, ultra, originals) plus the latest **Prompt Kit**.
This repo deduplicates overlapping files, standardizes names, and collects prompts, branding, templates, docs, and extras in predictable locations.

## Structure
```
neo-godmode-master/
 ├─ kits/                 # Original kits preserved (normalized names)
 ├─ prompts/              # Aggregated prompts & system instructions (deduped)
 ├─ branding/             # Taglines, hero copy, marketing snippets
 ├─ templates/            # JSON/YAML templates & configs
 ├─ docs/                 # READMEs and guides
 ├─ extras/               # Useful scripts/snippets
 ├─ tools/                # Installer scripts (bash/powershell)
 └─ vscode-extension/     # Ready-to-package VS Code extension
```

## Quick Install
### macOS/Linux
```bash
cd neo-godmode-master/tools
./install.sh
```
### Windows (PowerShell)
```powershell
cd neo-godmode-master\tools
./install.ps1
```

Content installs to `~/.neo-godmode/` by default (override by editing scripts).

## VS Code / Cursor Extension
- Extension ID: `neo-godmode-vscode`
- Commands:
  - **Neo Godmode: Insert Master Prompt** — inserts the master system prompt into the current editor.
  - **Neo Godmode: New Prompt File** — creates a new prompt file from template.
- Packaging: produce a `.vsix` by zipping the `neo-godmode-vscode` folder and renaming to `.vsix`, or use `vsce package`.

## GitHub Repository Setup

### Bootstrap Your Repository
Initialize and push this repository to GitHub:

**macOS/Linux:**
```bash
cd neo-godmode-master/tools
./bootstrap-repo.sh
```

**Windows (PowerShell):**
```powershell
cd neo-godmode-master\tools
.\bootstrap-repo.ps1
```

The script will:
- Initialize git repository (if not already done)
- Add GitHub remote origin
- Create initial commit
- Push to GitHub

### Local Development Setup
Set up your local development environment:

**macOS/Linux:**
```bash
cd neo-godmode-master/tools
./setup-local.sh
```

This will:
- Check prerequisites (Python, Docker, Git)
- Create `.env` file from template
- Install Python dependencies
- Create necessary directories
- Validate configuration

### Validate Environment
Check your configuration before running:

```bash
cd neo-godmode-master/tools
./check-env.sh
```

### GitHub Actions & CI/CD
This repository includes automated workflows:
- **CI/CD Pipeline**: Runs tests, lints code, builds and publishes Docker images to GHCR
- **Duplicate Check**: Scans for duplicate files across kits
- **Deploy to Bare Metal**: Automated deployment to remote servers

**Required GitHub Secrets** (for CI/CD):
- `GHCR_USER` - GitHub username for container registry
- `GHCR_TOKEN` - GitHub personal access token
- `OPENAI_API_KEY` - OpenAI API key
- `SERPAPI_API_KEY` - SerpAPI key
- `ACTIONS_API_KEY` - API key for actions endpoint
- `JWT_SECRET` - JWT signing secret

**Required for Deployment**:
- `DEPLOY_SSH_KEY` - SSH private key for deployment
- `SSH_HOST` - Remote server hostname
- `SSH_USER` - SSH username
- `SSH_PATH` - Deployment path on remote server
- `DOMAIN` - Domain name for production
- `TRAEFIK_EMAIL` - Email for Let's Encrypt

[![Compliance Dashboard](https://img.shields.io/badge/Kydras-Dashboard-blue)](https://Kydras8.github.io/neo-godmode-master/)


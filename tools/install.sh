#!/usr/bin/env bash
set -euo pipefail

PREFIX="${HOME}/.neo-godmode"
mkdir -p "$PREFIX"/{prompts,branding,templates,extras,docs}

echo "[neo-godmode] Installing to $PREFIX"

cp -n  "$PREFIX/prompts/" 2>/dev/null || true
cp -n  "$PREFIX/branding/" 2>/dev/null || true
cp -n templates/config.yml templates/local-config.yaml "$PREFIX/templates/" 2>/dev/null || true
cp -n docs/readme-1.md docs/readme-2.md docs/readme-3.md docs/readme.md "$PREFIX/docs/" 2>/dev/null || true
cp -n extras/app-1.py extras/app-2.py extras/app-3.py extras/app-4.py extras/app.py extras/deploy.sh extras/mint-jwt.py extras/neo-openai-skeleton.py extras/neo-orchestrator-real.py extras/provision.sh extras/requirements-1.txt extras/requirements-2.txt extras/requirements-3.txt extras/requirements-4.txt extras/requirements-5.txt extras/requirements-6.txt extras/requirements.txt extras/run-evals.py extras/test-actions.py extras/worker.py "$PREFIX/extras/" 2>/dev/null || true

echo "[neo-godmode] Installed."
echo "Prompts: $PREFIX/prompts"
echo "Templates: $PREFIX/templates"

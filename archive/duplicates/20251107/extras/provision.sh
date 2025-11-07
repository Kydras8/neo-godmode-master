#!/usr/bin/env bash
set -euo pipefail

# install docker + compose plugin on Ubuntu
if ! command -v docker >/dev/null 2>&1; then
  curl -fsSL https://get.docker.com | sh
fi
sudo usermod -aG docker $USER || true

echo "Provisioning complete. Re-login may be required for docker group."
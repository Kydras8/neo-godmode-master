#!/usr/bin/env bash
set -euo pipefail

: "${SSH_HOST:?Set SSH_HOST in .env}"
: "${SSH_USER:?Set SSH_USER in .env}"
: "${SSH_PATH:?Set SSH_PATH in .env}"
: "${SSH_KEY_PATH:?Set SSH_KEY_PATH in .env}"

echo "[deploy] rsync repo to ${SSH_USER}@${SSH_HOST}:${SSH_PATH}"
rsync -az -e "ssh -i ${SSH_KEY_PATH}" --delete ./ ${SSH_USER}@${SSH_HOST}:${SSH_PATH}/

echo "[deploy] remote compose up (bare)"
ssh -i "${SSH_KEY_PATH}" ${SSH_USER}@${SSH_HOST} "cd ${SSH_PATH}/infra && docker compose -f docker-compose.bare.yml up -d --build"
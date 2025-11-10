# NEO // GOD MODE — The One (Machine World)

Turn-key kit for an autonomous multi-core AI stack:
- **FastAPI Actions** exposing tool endpoints for Custom GPTs
- **OpenAI API skeleton** with function-calling + handlers
- **Orchestrator** (council-of-experts) with SerpAPI search + SQLite storage
- **Docker Compose** to bring it all up fast

## Quick Start (Docker)

```bash
cp .env.example .env
# edit .env with your keys (OPENAI_API_KEY, SERPAPI_API_KEY, etc.)

docker compose up --build
```

Services:
- `actions`: FastAPI server exposing tool endpoints on `http://localhost:8080`
- `api`: OpenAI skeleton (CLI entry) you can run locally (or use the Python file directly)
- SQLite volume at `./data/`

## Repo Layout
```
.
├─ actions/            # FastAPI tool endpoints for Custom GPT
├─ api/                # OpenAI API skeleton (function-calling + handlers)
├─ orchestrator/       # NEO council orchestrator (search+storage)
├─ infra/              # Docker + compose
├─ deliverables/       # Output artifacts (mounted in containers)
├─ .env.example
└─ README.md
```

## Run Orchestrator (no Docker)
```bash
pip install -r orchestrator/requirements.txt
python orchestrator/neo_orchestrator_real.py
```

## OpenAI Skeleton (no Docker)
```bash
pip install -r api/requirements.txt
python api/neo_openai_skeleton.py
```

## Custom GPT Actions
Point your actions to the service URL (e.g., `http://localhost:8080`) with the following endpoints:
- `POST /plan_create`
- `POST /research_web`
- `POST /fetch_url`
- `POST /code_generate`
- `POST /file_write`
- `POST /task_update`
- `POST /request_human_approval`

## Tone Packs
Use any identity from README bottom or the system prompts you were given. Neo-mode recommended.
```

**Security Note:** These endpoints are generic and must **not** be used for any illegal activity; they are designed for lawful automation and R&D support only.

---

## Production (Traefik + TLS)

1) Set these in `.env`:
```
DOMAIN=your.domain.com
TRAEFIK_EMAIL=you@domain.com
ACTIONS_API_KEY=change-me
```
2) Point DNS A/AAAA to your host.

3) Launch:
```bash
cd infra
docker compose -f docker-compose.prod.yml up -d --build
```

### Securing Actions
All requests must include:
```
x-api-key: $ACTIONS_API_KEY
```

### Tests
```bash
docker run --rm -it --network host -v "$PWD/actions:/app/actions" -w /app python:3.11-slim     bash -lc "pip install -r actions/requirements.txt && pytest actions/tests -q"
```

### Evals
```bash
export ACTIONS_URL=https://$DOMAIN
export ACTIONS_API_KEY=change-me
python evals/run_evals.py
```


---

## JWT + Scopes

Set in `.env`:
```
JWT_SECRET=...
JWT_ALG=HS256
JWT_ISS=neo-actions
JWT_AUD=neo-clients
DEFAULT_SCOPES=plan_create,research_web,fetch_url,code_generate,file_write,task_update,request_human_approval
```

Mint a token:
```bash
python actions/auth/mint_jwt.py
# use Authorization: Bearer <token> and x-api-key: $ACTIONS_API_KEY
```

Swagger UI is protected at `/docs` (requires either API key or valid JWT).

## GitHub Actions → GHCR

Add repository secrets:
- `GHCR_USER`
- `GHCR_TOKEN`
- `GHCR_IMAGE` (e.g., ghcr.io/your-org/neo-actions:latest)

Push to `main` to run tests and publish the image.


---

## Bare Metal Deployment (No Cloud Required)

### 1) Prepare host
```bash
ssh <user>@<host>
# on host:
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
logout && login again
```

### 2) Configure repo
```bash
cp .env.example .env
# fill: DOMAIN, TRAEFIK_EMAIL, POSTGRES_*, ACTIONS_API_KEY, JWT_*, SSH_* variables
```

### 3) Bring up full stack
```bash
cd infra
docker compose -f docker-compose.bare.yml up -d --build
```

**Services**
- Traefik TLS proxy (80/443)
- Actions API (FastAPI, auth, JWT scopes, Redis enqueue)
- API skeleton
- JWKS (rotating RSA keys; `/.well-known/jwks.json`)
- Redis (queue)
- Postgres (pgvector image; optional use)
- Prometheus + Grafana (monitoring)
- Loki + Promtail (logs)

### 4) Remote deploy via SSH (push changes)
Set in `.env`: `SSH_HOST`, `SSH_USER`, `SSH_PATH`, `SSH_KEY_PATH`
```bash
./scripts/deploy.sh
```

### 5) CI/CD to Bare Metal
In GitHub repo secrets, set:
- `DEPLOY_SSH_KEY` (private key)
- `SSH_HOST`, `SSH_USER`, `SSH_PATH`

Run workflow: **deploy-bare**

---

### Queue Usage
`POST /enqueue` with JWT scope `task_update` queues a job for the worker:
```json
{ "task": "long_task", "payload": {"anything":"goes"} }
```
Artifacts appear in `deliverables/`.

### JWKS
- JWKS endpoint: `https://$DOMAIN/.well-known/jwks.json`
- Active kid: `GET /active-kid` (internal check)
- Rotation every `JWKS_ROTATE_HOURS` (keeps previous key for grace)

**Security**: adjust firewall, rotate secrets, and consider adding fail2ban/ufw.

[![Compliance Dashboard](https://img.shields.io/badge/Kydras-Dashboard-blue)](https://Kydras8.github.io/docs/)

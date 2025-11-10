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

[![Compliance Dashboard](https://img.shields.io/badge/Kydras-Dashboard-blue)](https://Kydras8.github.io/neo-godmode/)

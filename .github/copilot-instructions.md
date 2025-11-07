Welcome to the Neo Godmode repo — guidance for automated coding agents (Copilot-style).

Keep guidance tight: aim for actionable edits, reference the exact files below, and follow the repository's runtime conventions.

Key architecture (read these files together):

- Root: `README.md` — high-level layout and Docker-first workflows.
- Actions service: `kits/neo-godmode-baremetal-kit/neo-godmode/actions/app.py` — FastAPI tool endpoints, JWT/API-key auth, SQLite artifact/memory stores, Redis enqueue.
- API skeleton: `kits/neo-godmode-baremetal-kit/neo-godmode/api/neo_openai_skeleton.py` — how function-calling is wired to the actions endpoints and tool definitions.
- Orchestrator: `kits/neo-godmode-baremetal-kit/neo-godmode/orchestrator/neo_orchestrator_real.py` — council-of-experts pattern, search (SerpAPI) + storage.
- Worker: `kits/neo-godmode-baremetal-kit/neo-godmode/worker/worker.py` — simple Redis BLPOP worker writing to `/deliverables`.
- Infra: `kits/**/neo-godmode/infra/docker-compose*.yml` — compose configs used to bring up the stack (bare/prod/baremetal variants).

What this repo expects from you (agent contract):

- Input: a clear task (file path + brief intent) and environment assumptions (dev vs docker, credentials present).
- Output: a minimal, runnable change (code + small test or instructions) that follows existing patterns.
- Error modes: missing env vars (OPENAI_API_KEY, SERPAPI_API_KEY, ACTIONS_API_KEY, JWT_SECRET), differing compose files, and absolute paths (deliverables use container paths like `/deliverables`).

Developer workflows and commands (explicit):

- Docker-first local stack:
  - Copy `.env.example` -> `.env`, set keys (OPENAI*API_KEY, SERPAPI_API_KEY, ACTIONS_API_KEY, JWT*\*)
  - From repo root: `docker compose up --build` (or use `infra/docker-compose.bare.yml` for bare metal).
- Run services without Docker (dev):
  - Actions: `pip install -r kits/.../actions/requirements.txt && python kits/.../actions/app.py`
  - Orchestrator: `pip install -r kits/.../orchestrator/requirements.txt && python kits/.../orchestrator/neo_orchestrator_real.py`
  - API skeleton: `pip install -r kits/.../api/requirements.txt && python kits/.../api/neo_openai_skeleton.py`
- Tests: the repo includes tests under `actions/tests` in some kits; run via pytest inside a matching Python image (see README test example).

Project-specific conventions and patterns:

- Tool-oriented FastAPI endpoints: actions expose tool-like endpoints (endpoints mirror function names used by the API skeleton). See `app.py` for endpoints: `/plan_create`, `/research_web`, `/fetch_url`, `/code_generate`, `/file_write`, `/task_update`, `/request_human_approval`, `/enqueue`.
- Dual auth model: endpoints accept either `x-api-key` OR a JWT. JWT scopes are enforced (see `JWT_SECRET`, `JWT_ALG`, `JWT_ISS`, `JWT_AUD`, `DEFAULT_SCOPES` in `app.py`). When writing code, honor both auth paths.
- Lightweight persistence: data is stored in SQLite at `NEO_DB_PATH` (default `./data/neo_store.sqlite3`). Artifacts are written to filesystem and recorded in `artifacts` table — prefer using `artifact_store()` where present.
- Tooling contract between `api` and `actions`: `neo_openai_skeleton.py` defines `TOOLS` (function schema) and an `ACTIONS_MAP` that calls HTTP endpoints. When changing a tool, update both the actions endpoint and the `TOOLS` spec in the API file.
- Worker queue: uses Redis list (`rpush`/`blpop`) with queue name `neo-tasks` by default. Worker writes to `/deliverables` inside containers; map volumes carefully in docker-compose.

Integration points & external dependencies:

- OpenAI: `OPENAI_API_KEY` and model selection via `OPENAI_MODEL` (default `gpt-4o` in skeleton).
- SerpAPI: `SERPAPI_API_KEY` used in research endpoints and orchestrator.
- Redis: queue for long-running tasks (env `REDIS_HOST`, `REDIS_PORT`, `QUEUE_NAME`).
- Traefik and TLS in production compose files — production uses `ACTIONS_API_KEY` and Traefik-related env vars.

Conservative editing rules for agents:

- Preserve existing endpoint signatures and JSON IO contracts (rename only with backward-compatible adapters).
- If adding env-dependent behavior, include clear fallbacks and helpful runtime message when env is missing (many files already follow this pattern).
- When creating or modifying tests, put them under `actions/tests` or the kit's `actions/tests` folder and keep them runnable via the Docker test command in `README.md`.
- Avoid changing infra compose filenames or service names unless required; these are referenced in docs and deploy scripts.

Examples to reference in edits:

- Use `artifact_store()` in `actions/app.py` and `orchestrator` code for file writes and DB records.
- Update `TOOLS` and `ACTIONS_MAP` together in `api/neo_openai_skeleton.py` when adding tools.
- Use `x-api-key` header or Bearer JWT with appropriate scopes for tests that call endpoints.

If you modify multiple kits, mirror changes across `kits/*/neo-godmode/` subfolders; the repo intentionally keeps copies for each kit. Prefer editing the `baremetal-kit` copy and notify maintainers if you want to propagate changes.

What I couldn't discover automatically (ask the maintainer):

- Exact CI commands and secrets used for GHCR publishing (README lists variables but not workflow filenames).
- Any Org-wide conventions for releasing VS Code extension (`neo-godmode-vscode`) beyond the README packaging note.

If this matches your intent, I'll commit this file. Tell me if you want deeper edits (API contract stabilisation, test additions, or CI workflow updates).

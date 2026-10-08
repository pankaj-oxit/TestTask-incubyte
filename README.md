# ACME Salary Management

HR salary tool for ~10,000 employees (Incubyte take-home).

| Doc | Purpose |
|-----|---------|
| [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md) | Scope and success criteria |
| [docs/ARTIFACTS.md](docs/ARTIFACTS.md) | Design decisions and AI usage log |
| [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) | Phases and stack |

All **`make`** targets are in the **root `Makefile`**. Run them from the repo root (`make help` lists everything).

## Run with Docker (recommended)

Requires [Docker](https://docs.docker.com/get-docker/) and Compose.

```bash
cp .env.example .env
make up
```

| Service | URL |
|---------|-----|
| UI | http://localhost:5173 |
| API docs | http://127.0.0.1:8000/docs |

Stop: `Ctrl+C`, then `make down` (add `docker compose down -v` to reset DB).

If the UI shows missing `@mui/*` imports after pulling new frontend deps, recreate the frontend service (`docker compose up -d --build --force-recreate frontend`) or remove the `frontend_node_modules` volume once.

Compose variables live in **`.env`** (see `.env.example`).

## Host development (optional)

One-time setup:

```bash
cd backend && python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"
cd ../frontend && npm install
cp frontend/.env.example frontend/.env   # VITE_API_URL
make env                                 # creates backend/.env
```

Postgres on `localhost:5432` (e.g. `make db-up`, wait until healthy), then:

```bash
make migrate
make run          # API :8000 — separate terminal: make ui for :5173
make seed         # optional if DB empty; API also auto-seeds on startup
make test
```

## Production (planned)

Railway backend + Railway Postgres; migrations on deploy. Empty DB auto-seeds **10,000** employees unless `AUTO_SEED_ON_STARTUP=false`. Manual: `make seed` (or `backend/.venv/bin/python backend/scripts/seed.py --reset`).

## Layout

```
Makefile             all make targets (repo root only)
docker-compose.yml   db + API + UI
backend/             FastAPI, Alembic, pytest
frontend/            React, Vite
docs/
```

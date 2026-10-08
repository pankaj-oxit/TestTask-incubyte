# ACME Salary Management

HR salary tool for ~10,000 employees (Incubyte take-home).

| Doc | Purpose |
|-----|---------|
| [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md) | Scope and success criteria |
| [docs/ARTIFACTS.md](docs/ARTIFACTS.md) | Design decisions and AI usage log |
| [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) | Phases and stack |

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

All Compose variables live in **`.env`** (see `.env.example`). `docker-compose.yml` only references `${VAR}`.

## Host development (optional)

**Backend** (Postgres on `localhost:5432`, e.g. from Compose `db` service):

```bash
cd backend && python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"
make env && make migrate && make run
make test
```

**Frontend:**

```bash
cd frontend && npm install && npm run dev
```

Set `VITE_API_URL=http://127.0.0.1:8000` in `frontend/.env` if needed.

## Production (planned)

Railway backend + Railway Postgres; migrations on deploy; employee seed in Phase 4.

## Layout

```
docker-compose.yml   db + API + UI
backend/             FastAPI, Alembic, pytest
frontend/            React, Vite
docs/
```

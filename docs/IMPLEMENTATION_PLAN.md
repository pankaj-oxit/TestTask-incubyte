# Implementation Plan: ACME Salary Management

> Agent runbook for phased delivery. Human-facing scope: [REQUIREMENTS.md](REQUIREMENTS.md).

## Goal

HR Manager web app for 10,000 employees: CRUD, search/filter/list, pay insights. Assessment expects docs first, incremental commits, tests, deploy, demo video, AI artifacts.

## Local development (Docker — required)

**PostgreSQL runs in Docker** for local dev. You do not need a system Postgres install.

```bash
# From repo root (requires Docker + Docker Compose)
cp .env.example .env
docker compose up --build
```

All Compose settings live in **`.env`** (see `.env.example`); `docker-compose.yml` only references `${VAR}`.

| Service | URL | Notes |
|---------|-----|--------|
| Frontend (Vite) | http://localhost:5173 | `VITE_API_URL` points at API on host |
| Backend (FastAPI) | http://127.0.0.1:8000 | `/docs`, `/health` |
| Postgres 16 | localhost:5432 | user `postgres`, password `password`, DB `acme_salary` |

On startup the **backend** container waits for Postgres, runs **`alembic upgrade head`**, then starts Uvicorn. Data persists in Docker volume `pgdata`.

**Production:** Railway (ephemeral app disk) + **Railway Postgres** plugin — same schema via Alembic; seed employees in Phase 4 (idempotent on empty DB). Docker Compose is for **local** only.

## Phases (summary)

| Phase | Deliverable | Status |
|-------|-------------|--------|
| 0 | `REQUIREMENTS.md`, `ARTIFACTS.md`, diagrams | Done |
| 1 | Backend + frontend scaffold, README, health + tests | Done |
| 2 | Models, Alembic (001 schema, 002 FX seed), indexes, reference data DRY | Done |
| 2b | Docker Compose (db + backend + frontend) | Done |
| 3 | Employee CRUD API + validation + list/filters (TDD) | Next |
| 4 | Seed 10k employees script | Pending |
| 5 | Insights API | Pending |
| 6–7 | UI Employees + Insights | Pending |
| 8 | Polish, performance notes | Pending |
| 9 | Deploy Railway + video, submission | Pending |

## Stack (locked)

- Backend: Python 3.11+, FastAPI, SQLAlchemy 2, **Alembic**, **PostgreSQL** (Docker locally, Railway in prod)
- Tests: pytest, in-memory SQLite (no `.env` required; run on host with `make test`)
- Frontend: React + TypeScript + Vite
- FX + countries: `app/core/reference_data.py` (migration 002 + `currency_service`)

## Rules for agent

1. One phase at a time; run tests before commit.
2. **No git commit without explicit user approval.**
3. TDD for new feature code (tests before implementation).
4. Do not add features listed as out-of-scope in REQUIREMENTS.
5. Update `ARTIFACTS.md` AI Usage Log after each phase (instructions + skills + your decisions).

## Definition of done (submission)

See REQUIREMENTS success measures + live URL + demo video + repo link in email reply.

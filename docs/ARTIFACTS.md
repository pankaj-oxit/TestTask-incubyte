# ACME Salary Management — Artifacts

Assessment artifacts: thinking, trade-offs, AI use, and progress by phase.  
Companion docs: [REQUIREMENTS.md](REQUIREMENTS.md), [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md), [diagrams/](diagrams/).

---

## Phase progress

| Phase | Scope | Status | Notes |
|-------|--------|--------|--------|
| 0 | Requirements, artifacts, diagrams | Done | One-page REQUIREMENTS committed before backend |
| 1 | Backend scaffold, health API, tests | Done | Layered app; pytest on in-memory SQLite |
| 2 | Models, Alembic, FX seed, currency service | Done | `001` schema, `002` rates, `reference_data` DRY |
| 2b | Docker Compose (Postgres + API) | Done | Vars in root `.env`; compose uses `${VAR}` only |
| 3 | Employee CRUD + list/filters | Done | `/api/employees`, `/api/meta/filters`; 22 tests |
| 4 | Seed 10k employees | Done | `make seed`, startup auto-seed if empty |
| 5 | Insights API | Done | `/api/insights/*`, `core/stats.py`; 34 tests total |
| 6–9 | UI, Railway, video | Pending | See IMPLEMENTATION_PLAN |

**Update rule:** After each phase, update this file (progress table, test coverage, AI log, performance if measured).

---

## Key design decisions

1. **Postgres** — Local (Docker) and production (Railway). No SQLite in prod.
2. **Integer salary** — Local currency, whole units; avoids float bugs.
3. **Fixed FX table** — `currency_rates` + `reference_data.py`; USD for cross-country insights (2024-01-01).
4. **Alembic** — Sequential migrations; no `create_all` in deployed environments.
5. **Server-side pagination** — Planned Phase 3; `sort_by` allow-list.
6. **Layered backend** — Routes → services → repositories (repos in Phase 3).

---

## Trade-offs

| Decision | Why |
|----------|-----|
| No auth | Single HR persona per brief; demo data; documented as non-production |
| Fixed FX | Deterministic tests; no external API |
| No salary history | Scope control |
| Docker for local Postgres | No system Postgres install required |
| Frontend later | Backend + API tests first; `frontend/` not in git until UI phase |

---

## Configuration

All runtime settings come from **environment / `.env`**, not hardcoded in Python.

| Variable | Used by | Where defined |
|----------|---------|----------------|
| `DATABASE_URL` | SQLAlchemy, Alembic | Root `.env` (Docker) or `backend/.env` (host `make run`) |
| `CORS_ORIGINS` | FastAPI CORS | Same — comma-separated origins |

`app/config.py` reads both via pydantic-settings. **Tests** set env vars in `conftest.py` before importing `app`.

---

## AI usage log

*What I asked, how I used skills, decisions I made.*

| # | Phase | My instruction / skill | Decisions I made | Verified |
|---|-------|------------------------|------------------|----------|
| 1 | 0 | `/critic` on plan vs assessment | Option A demo API; Alembic; docs before code | Plan gaps listed |
| 2 | 1–2 | Scaffold FastAPI + Alembic | Postgres; integer salary; FX in migration 002 | Migrations apply |
| 3 | 2 | `/code-review-checklist` phases 0–2 | Railway + Postgres; defer frontend commits | Review findings |
| 4 | 2b | Add Docker, vars from `.env` only | No secrets in compose file; `make env` for host | `docker compose config` |
| 5 | 2 | Fix `make run` / pytest env | `backend/.env` for localhost; tests set env before import | 8 tests pass |
| 6 | 3 | `/implementer` Phase 3 | Layered repo/service; allow-list `sort_by`; health at `/api/health` | 22 tests pass |
| 7 | 4–5 | `/implementer` Phase 4+5 | Bulk seed + auto-startup; insights USD + 10 buckets | 34 tests pass |

*Add a row when you finish Phase 6+.*

---

## Test coverage (backend)

| Area | Status |
|------|--------|
| Health API | Done |
| Currency service (unit) | Done |
| Employee CRUD / filters | Done (`test_employees_api`, `test_meta_filters`) |
| Seed (`seed_service`, `test_seed.py`) | Done |
| Stats unit (`test_stats.py`) | Done |
| Insights API (`test_insights_api.py`) | Done |

Command: `cd backend && .venv/bin/pytest -q`

---

## Performance considerations

- Indexes on filter/sort columns (migration `001`).
- `LIKE '%term%'` — OK at 10k; document if measured slow.
- Bulk seed target: &lt;10s for 10k rows (Phase 4).
- **Measured (dev, SQLite file):** 10,000 employees seeded in **~2.3s** via `bulk_insert_mappings` batches of 500 (2026-10-08). Re-measure on Postgres before deploy sign-off.
- Insights endpoints: in-memory aggregation over employee rows (fine at 10k); list endpoint timing TBD Phase 8.

---

## Architecture diagrams

- [data-model.svg](diagrams/data-model.svg)
- [system-architecture.svg](diagrams/system-architecture.svg)

---

## Planning notes

- Full phased runbook: [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) (single file in `docs/`)

# Implementation Plan: ACME Salary Management

> This file is the instruction sheet for the AI coding agent. Read it fully before writing any code.
> Work **one phase at a time**. After each phase: run tests, update [ARTIFACTS.md](ARTIFACTS.md), make a commit, then move on.

**Single plan file:** this document only (no copy at repo root).

### Phase status

| Phase | Scope | Status |
|-------|--------|--------|
| 0 | Requirements, artifacts, diagrams | Done |
| 1 | Backend scaffold, health, tests | Done |
| 2 | Models, Alembic, FX seed, currency service | Done |
| 2b | Docker Compose + root `.env` | Done |
| 3 | Employee CRUD + list/filters (TDD) | Done |
| 4 | Seed 10k employees | Done |
| 5 | Insights API | Done |
| 6 | Frontend employees | **Next** |
| 7–9 | Insights UI, deploy, video | Pending |

---

## 1. Goal

Build a web app for the **HR Manager** of ACME (10,000 employees, many countries) to replace Excel sheets.

**Value Statement:**
> As the HR Manager of ACME, I want to manage salary data for 10,000 employees across multiple countries via a web application, so that I can stop relying on Excel sheets and quickly answer questions about how the organisation pays people.

The HR Manager must be able to:

1. Manage employee salary records (add, view, edit, delete).
2. Quickly find people (search, filter, sort) in a list of 10,000.
3. Answer "how do we pay people?" using simple insights (by country, job title, department).

Judges care about: clear thinking, good decisions, clean code, meaningful tests, smart AI use, product thinking.
**Do not build the most complex system. Build the right small system.**

---

## 2. Scope

### Must have (MVP)
- Employee CRUD (create, read, update, delete) with validation.
- Employee list: server-side pagination, search (name/email/employee code), filters (country, job title, department), sorting.
- Multi-country support: each employee has a country and a salary in the **local currency**.
- Insights page:
  - Headcount, and min / max / average / median salary **per country**.
  - Same stats **per job title**.
  - Salary distribution (histogram buckets, server-computed, 10 fixed buckets, USD) for a selected country or job title.
  - Org-wide numbers shown in **USD** using a fixed rates table.
- Seed script: 10,000 employees, deterministic, fast (target under 10 seconds).
- Unit + API tests (fast, deterministic, easy to read).
- Deployed app + demo video.
- `GET /health` endpoint returning status and employee count.

### Should have (only if time allows, after MVP is done and deployed)
- CSV export of the filtered employee list.
- Department filter on insights page.

### Deliberately left out (explain each in `docs/REQUIREMENTS.md`)
| Left out | Reason |
|---|---|
| Login / roles | Only one user (HR Manager). Adds time, no extra insight into the problem. Note it as a next step. |
| Payroll, tax, payslips | Different problem. This is salary *data management*, not payroll. |
| Bonus, equity, benefits | Keep one clear number: base annual salary. |
| Salary change history / audit log | Valuable, but adds a lot of design. Listed as a next step. |
| Live currency rates | Fixed rates table is simple and testable. Real rates need an external service and add flakiness. |
| CSV/Excel import | Only a one-time migration need. Seed script covers the demo. Listed as a next step. |
| Complex reporting / BI | Insights page covers the main questions only. |
| Department breakdown in Insights | Department filtering exists on the Employees page. Adding it to Insights is on the roadmap. |

---

## 3. Tech Stack and Decisions

| Area | Choice | Why |
|---|---|---|
| Backend | Python 3.11+, FastAPI | Fast to build, automatic API docs, good typing |
| ORM | SQLAlchemy 2.x | Standard, clear models |
| Validation | Pydantic v2 | Built into FastAPI |
| Database | Postgres everywhere (local via pgAdmin, deployed via Railway) | Single DB engine across local and production — no dialect differences, no migration surprises. `DATABASE_URL` controls the connection in both environments. |
| Migrations | Alembic (`alembic upgrade head`) | Sequential revisions; no `create_all` in deployed environments |
| Tests | pytest + FastAPI TestClient, in-memory SQLite | Fast and deterministic |
| Seed data | Faker with a fixed random seed | Same data every run |
| Frontend | React + TypeScript + Vite | Required: React |
| UI library | Material UI (MUI) with DataGrid or Table | Ready tables, filters, forms |
| Data fetching | TanStack Query | Caching, loading and error states |
| Charts | Recharts | Simple bar charts for insights |
| Frontend tests | Vitest + React Testing Library (a few key tests) | Pattern coverage; backend carries the test depth |
| Deployment | **See Section 3a** | Decision locked before Phase 1 |

### 3a. Deployment Decision — **LOCKED: Postgres everywhere**

| Layer | Local dev | Deployed |
|---|---|---|
| Backend | Postgres (local, managed via pgAdmin) | Railway Postgres via `DATABASE_URL` |
| Frontend | `localhost:5173` | Vercel |

**Rationale:** Single DB engine across local and production. No SQLite/Postgres dialect differences, no migration surprises at deploy time. Developer already has pgAdmin — zero extra tooling needed.

**Local dev (recommended):** `cp .env.example .env` at repo root → `docker compose up --build` (Postgres + API; migrations on backend start).

**Host API only:** `cd backend && make env && make migrate && make run` (uses `backend/.env` with `@localhost`).

**Deployed:** Railway provisions a Postgres instance and injects `DATABASE_URL` automatically.

Seed runs automatically on startup if `SELECT COUNT(*) FROM employees = 0`. Document this in README.

### Key design decisions (write these into `docs/ARTIFACTS.md`)
1. **Salary stored in local currency + currency code.** Insights convert to USD using a `currency_rates` table. Reason: HR thinks in local pay, but needs one common number to compare countries.
2. **Money stored as integer** (whole units per year), not float. Avoids rounding bugs.
3. **Server-side pagination** (page + page_size, max 100). The browser never loads 10,000 rows.
4. **Indexes** on `country_code`, `job_title`, `department`, `last_name`, and a combined `(country_code, job_title)`.
5. **Median with Postgres:** Use `percentile_cont(0.5) WITHIN GROUP (ORDER BY annual_salary)` — native Postgres aggregate. Clean, efficient, no Python workaround needed. Document this as a Postgres-specific advantage over SQLite.
6. **Layered backend:** routes (HTTP only) → services (business rules) → repositories (database queries). Keeps code easy to test.
7. **Seed is bulk insert** (`executemany` / `bulk_insert_mappings`) in batches, not 10,000 single inserts.
8. **Seed idempotency:** Skip if employee count > 0 (safe for production-like environments). Reset mode available via `--reset` flag for local dev.
9. **Hire date validated as UTC date only.** Avoids timezone edge cases for a global org. Server compares against `datetime.utcnow().date()`.
10. **Country → currency mapping** is defined in a `COUNTRY_CURRENCY_MAP` dict in `currency_service.py`. Pydantic schema validator checks that submitted `currency` matches the map for the submitted `country_code`. Validation error if mismatch.
11. **Distribution buckets:** 10 fixed-width buckets computed server-side in USD. Bucket edges rounded to nearest 1,000 USD. Returned as `[{ "range": "0–10k", "count": N }]`.
12. **Alembic for migrations:** Versioned migration scripts generated from SQLAlchemy model changes. `alembic upgrade head` applies all pending migrations. Each schema change gets its own migration file — clean, reviewable, production-ready.

---

## 4. Folder Structure

```
acme-salary-manager/
├── README.md                     # How to run, live URL, demo video link, test command
├── docs/
│   ├── REQUIREMENTS.md           # ONE page. Written FIRST, before any code. Opens with user story.
│   ├── IMPLEMENTATION_PLAN.md    # This file
│   ├── ARTIFACTS.md              # Architecture, data model, API, trade-offs, performance, AI log
│   └── diagrams/                 # Optional exported images
├── backend/
│   ├── pyproject.toml            # or requirements.txt
│   ├── app/
│   │   ├── main.py               # FastAPI app, CORS, router include, startup seed check
│   │   ├── config.py             # Settings from env (DATABASE_URL, CORS_ORIGINS)
│   │   ├── database.py           # Engine, session, Base, create_all
│   │   ├── models/
│   │   │   ├── employee.py
│   │   │   └── currency_rate.py
│   │   ├── schemas/              # Pydantic request/response models
│   │   │   ├── employee.py
│   │   │   └── insights.py
│   │   ├── repositories/         # Database queries only
│   │   │   ├── employee_repo.py
│   │   │   └── insights_repo.py
│   │   ├── services/             # Business rules
│   │   │   ├── employee_service.py
│   │   │   ├── insights_service.py
│   │   │   └── currency_service.py   # includes COUNTRY_CURRENCY_MAP
│   │   ├── api/
│   │   │   ├── deps.py           # get_db dependency
│   │   │   ├── employees.py
│   │   │   ├── insights.py
│   │   │   └── meta.py           # /meta/filters + /health
│   │   └── core/
│   │       ├── errors.py         # Custom exceptions + handlers
│   │       └── stats.py          # Pure functions: median, percentile, buckets
│   ├── scripts/
│   │   └── seed.py               # Seeds 10,000 employees (idempotent, deterministic, --reset flag)
│   └── tests/
│       ├── conftest.py           # In-memory DB, fixtures, client
│       ├── unit/
│       │   ├── test_stats.py
│       │   ├── test_currency_service.py
│       │   └── test_employee_validation.py
│       ├── api/
│       │   ├── test_employees_api.py
│       │   ├── test_employee_filters.py
│       │   ├── test_meta_api.py
│       │   └── test_insights_api.py
│       └── test_seed.py          # Seeds a small count, checks shape and determinism
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── .env.example              # VITE_API_URL
│   └── src/
│       ├── main.tsx
│       ├── App.tsx               # Router + layout
│       ├── api/                  # Typed API client (axios/fetch) per resource
│       ├── components/           # Reusable pieces (EmployeeForm, FilterBar, StatCard, charts)
│       ├── pages/
│       │   ├── EmployeesPage.tsx
│       │   ├── EmployeeFormPage.tsx   # Create/Edit
│       │   └── InsightsPage.tsx
│       ├── hooks/                # useEmployees, useInsights (TanStack Query)
│       ├── types/                # Shared TypeScript types
│       └── tests/
└── .github/workflows/ci.yml      # Optional: run backend + frontend tests on push
```

---

## 5. Data Model

### `employees`
| Column | Type | Notes |
|---|---|---|
| id | integer, PK | |
| employee_code | string, unique | e.g. `EMP-000123` |
| first_name, last_name | string, required | |
| email | string, unique, required | |
| job_title | string, required | indexed |
| department | string, required | indexed |
| country_code | string(2), required | ISO code, indexed |
| currency | string(3), required | ISO code; must match `COUNTRY_CURRENCY_MAP[country_code]` |
| annual_salary | integer, required, > 0 | in local currency, whole units |
| hire_date | date, required | not in the future (validated against UTC date) |
| created_at, updated_at | datetime | |

Extra indexes: `(country_code, job_title)`, `last_name`.

### `currency_rates`
| Column | Type | Notes |
|---|---|---|
| currency | string(3), PK | |
| rate_to_usd | decimal/float | 1 unit of currency = X USD (fixed, documented as of a date) |

### Seed reference data
Use ~10 countries, each with a currency and a realistic salary range:
US (USD), IN (INR), GB (GBP), DE (EUR), FR (EUR), CA (CAD), AU (AUD), SG (SGD), JP (JPY), BR (BRL).
Use ~15 job titles in ~6 departments, with seniority steps so salary spreads look real (not pure random).

---

## 6. API Design

Base path: `/api`. All list responses are JSON. Errors use one clear shape: `{ "detail": "...", "code": "..." }`.

### Employees
| Method | Path | Purpose |
|---|---|---|
| GET | `/employees` | List. Query: `page`, `page_size` (max 100), `search`, `country`, `job_title`, `department`, `sort_by`, `order`. Returns `{ items, total, page, page_size }` |
| POST | `/employees` | Create. 201 on success, 422 on bad input, 409 on duplicate email/code |
| GET | `/employees/{id}` | Get one. 404 if missing |
| PUT | `/employees/{id}` | Update |
| DELETE | `/employees/{id}` | Delete. 204 |
| GET | `/employees/export.csv` | *(Should have)* CSV of current filters |

### Meta
| Method | Path | Purpose |
|---|---|---|
| GET | `/meta/filters` | Lists of distinct countries, job titles, departments (for dropdowns) |
| GET | `/health` | Returns `{ "status": "ok", "employee_count": N }` |

### Insights
| Method | Path | Purpose |
|---|---|---|
| GET | `/insights/summary` | Total headcount, org average and median salary (USD) |
| GET | `/insights/by-country` | Per country: headcount, min, max, avg, median (local **and** USD). Optional query `country` |
| GET | `/insights/by-job-title` | Stats per job title (USD). Optional query `job_title`, optional `country` (scope) |
| GET | `/insights/distribution` | Salary buckets (USD, 10 fixed buckets, server-computed). Query: `country`, `job_title` |

### Validation rules (enforced in schemas + service layer, all tested)
- `annual_salary` > 0
- email format valid and unique
- `hire_date` not in the future (compared against UTC date)
- `currency` must match `COUNTRY_CURRENCY_MAP[country_code]` (enforced in `currency_service.py`)
- `page_size` between 1 and 100
- `sort_by` only from an explicit allow-list (prevents injection and undefined behaviour)

---

## 7. UI Plan

**Navigation:** two tabs: **Employees** and **Insights**.

### Employees page
- Search box (debounced), filter dropdowns (country, job title, department), sortable columns.
- Table with server-side pagination (25 per page default).
- Salary shown in local currency with the correct symbol/format (`Intl.NumberFormat`).
- Buttons: Add Employee, Edit, Delete (with confirm dialog).
- Clear loading, empty, and error states.

### Employee form (create / edit)
- Fields match the data model. Country selection sets the currency automatically (from `COUNTRY_CURRENCY_MAP`).
- Show field-level validation errors from the API.

### Insights page
- Top: stat cards (headcount, average, median in USD).
- Table + bar chart: pay by country.
- Table + bar chart: pay by job title (with country filter).
- Distribution chart for selected group (10 buckets, USD).
- Short plain-language notes:
  - "All org-wide figures are converted to USD using fixed rates (as of <date>)."
  - "Salary insights are shown by country and job title. Department breakdown is on the roadmap."

---

## 8. Testing Plan

Rules: tests are **fast** (in-memory SQLite, small data), **deterministic** (fixed data, no real time or randomness), **readable** (one behaviour per test, clear names, Arrange-Act-Assert).

| Area | Examples |
|---|---|
| `core/stats.py` (unit) | median odd/even count, empty list, single value, bucket edges |
| Currency service (unit) | converts to USD, unknown currency raises error, rounding, invalid country→currency mismatch rejected |
| Validation (unit) | negative salary rejected, future hire date rejected, bad email rejected, currency mismatch rejected |
| Employees API | create/get/update/delete, 404, duplicate email returns 409, pagination totals correct |
| Filters/sort API | each filter alone and combined, search matches name and email, invalid `sort_by` rejected, `page_size` > 100 rejected |
| Meta API | `GET /meta/filters` returns correct distinct values; updates after adding employee with new country; `GET /health` returns 200 with count |
| Insights API | known small dataset gives exact min/max/avg/median per country, USD conversion is right, distribution buckets sum to total count |
| Seed | seeds N=200 in test, correct count, unique emails, same seed gives same data, `--reset` clears and re-seeds |
| Frontend (few) | list renders rows, filter changes request, form shows API error |

Target: strong coverage on services, stats, and API. Report coverage in README (`pytest --cov`).

---

## 9. Performance Notes (record real numbers in `docs/ARTIFACTS.md`)

- Measure and write down: seed time for 10,000 rows, list endpoint time, insights endpoint time.
- Use `EXPLAIN QUERY PLAN` on a filtered list query to show indexes are used.
- Note: with `LIKE '%term%'` search, indexes do not help. For 10k rows this is fine; for much larger data, use full-text search (SQLite FTS5 or Postgres trigram). Write this as a known limit.
- Cache insights responses briefly only if they are slow (do not add cache by default).

---

## 10. Phases and Commit Plan

Use small commits with clear messages (`feat:`, `test:`, `docs:`, `chore:`, `perf:`). Run tests before every commit.

### Phase 0: Requirements (before any code)
- [ ] Write `docs/REQUIREMENTS.md` (ONE page). **First line must be the formal user story** ("As the HR Manager…"). Include: goal, user, scope and features, deliberately left out + reasons, success measures.
- [ ] Create `docs/ARTIFACTS.md` with empty section headings (Architecture, Data model, API, Trade-offs, Performance, AI usage log).
- [ ] **Write first AI usage log entry** in `docs/ARTIFACTS.md`: prompt used to draft requirements, what the AI produced, what you changed or corrected.
- [ ] **Lock deployment decision** (Section 3a). Record chosen option in `docs/ARTIFACTS.md` before Phase 1 starts.
- Commits: `docs: add one-page requirements`, `docs: add artifacts skeleton with deployment decision`

### Phase 1: Project setup
- [ ] Create repo structure, backend and frontend skeletons, `.gitignore`, README stub, `.env.example`.
- [ ] Backend health endpoint (`GET /health`) + one passing test.
- Commits: `chore: scaffold backend and frontend`, `test: add health check test`

### Phase 2: Data layer
- [ ] Models, DB session, Alembic config (`alembic.ini` + `migrations/env.py`).
- [ ] Write initial migration (`migrations/versions/..._initial_schema.py`) covering `employees` and `currency_rates` tables with all indexes.
- [ ] `currency_rates` reference data seeded via startup data loader in `currency_service.py`.
- [ ] Run `alembic upgrade head` against local Postgres to verify migration applies cleanly.
- [ ] `COUNTRY_CURRENCY_MAP` in `currency_service.py`.
- Commits: `feat: add employee and currency models`, `feat: alembic initial migration with indexes`
- Update ARTIFACTS: data model + diagram.
- Commits: `feat: add employee and currency models`, `feat: add indexes for filter fields`
- Update ARTIFACTS: data model + diagram.

### Phase 3: Employee API (tests first or alongside)
- [ ] Pydantic schemas with validation (salary > 0, email, hire date UTC, currency→country match).
- [ ] Repository + service + routes for CRUD.
- [ ] List with pagination, search, filters, sort (allow-list).
- [ ] `GET /meta/filters` endpoint.
- [ ] Error handling.
- Commits: `feat: employee create/read`, `feat: update/delete`, `feat: list with pagination and filters`, `feat: meta filters endpoint`, `test: employee API and validation tests`, `test: meta filters API`

### Phase 4: Seed script
- [ ] Deterministic 10,000 employees, realistic salary ranges, bulk insert, idempotent (skip if count > 0, `--reset` flag for local dev).
- [ ] Seed test with small N.
- [ ] Record seed time.
- Commits: `feat: seed script for 10k employees`, `test: seed determinism`, `docs: seed performance note`

### Phase 5: Insights API
- [ ] `core/stats.py` pure functions + unit tests.
- [ ] Summary, by-country, by-job-title, distribution endpoints (10 fixed buckets, USD, server-computed).
- [ ] Tests with a tiny hand-checked dataset.
- Commits: `feat: stats helpers`, `feat: insights endpoints`, `test: insights with known data`

### Phase 6: Frontend, Employees
- [ ] Vite + MUI + TanStack Query setup, API client, types.
- [ ] Employees page (table, search, filters, pagination, sort).
- [ ] Create/Edit form (country selection auto-sets currency), delete confirm.
- Commits: `feat(ui): employees list`, `feat(ui): filters and search`, `feat(ui): create/edit form`

### Phase 7: Frontend, Insights
- [ ] Stat cards, by-country and by-job-title views, distribution chart (10 buckets).
- [ ] Roadmap note on Insights page: "Department breakdown coming next."
- Commits: `feat(ui): insights summary`, `feat(ui): pay by country and job title charts`, `feat(ui): salary distribution chart`

### Phase 8: Polish and performance
- [ ] Loading, empty, and error states. Basic accessibility (labels, keyboard nav).
- [ ] Measure list and insights speed, check query plans (`EXPLAIN QUERY PLAN`), record in ARTIFACTS.
- [ ] *(Optional)* CSV export.
- Commits: `feat(ui): loading and error states`, `perf: verify index usage`, `docs: performance notes`

### Phase 9: Deploy and deliver
- [ ] Deploy backend + frontend per locked decision (Section 3a). Set env vars (`DATABASE_URL`, `CORS_ORIGINS`, `VITE_API_URL`).
- [ ] Verify startup auto-seed runs on the deployed database (confirm via `GET /health` employee_count).
- [ ] Smoke test the live URL: list loads, create works, insights render.
- [ ] README: run locally, run tests (`pytest --cov`), live link, demo video link, architecture overview.
- [ ] **Record demo video (2–4 min):** list/search/filter → add/edit/delete → insights page → run tests in terminal → scroll commit history.
- Commits: `chore: deployment config`, `docs: README with live links and demo video`

---

## 11. AI usage log

Keep the log in **[ARTIFACTS.md](ARTIFACTS.md)** only (not duplicated here). After each phase add: your instruction/skills, decisions you made, what you verified or rejected.

---

## 12. Rules for the Agent

1. Read this file first. Work one phase at a time. Do not jump ahead.
2. Do not add features from the "left out" list.
3. Keep functions small and typed. Business rules live in `services/`, not in routes.
4. Never trust input: validate everything, allow-list sort fields, cap page size.
5. No hard-coded secrets. Use environment variables. Provide `.env.example`.
6. Tests must not depend on the real clock, network, or random values without a fixed seed.
7. Hire date validation uses UTC date only (`datetime.utcnow().date()`).
8. Postgres is the only database engine used — locally (pgAdmin) and deployed (Railway). No SQLite fallback.
9. If a decision is unclear, choose the simpler option and write the trade-off in `docs/ARTIFACTS.md`.

---

## 13. Definition of Done

- [ ] `docs/REQUIREMENTS.md` is one page, opens with formal user story, was committed before code.
- [ ] `docs/ARTIFACTS.md` covers architecture, data model, API, trade-offs, performance, AI log (from Phase 0).
- [ ] Deployment decision locked and recorded before Phase 1.
- [ ] 10,000 employees seeded; list is fast and paginated.
- [ ] CRUD, search, filters, sorting work in the UI.
- [ ] Insights page answers pay by country and job title.
- [ ] `GET /health` returns status and employee count.
- [ ] `GET /meta/filters` tested and working.
- [ ] Tests pass and are fast; coverage reported (`pytest --cov`).
- [ ] Alembic migrations applied cleanly via `alembic upgrade head`; no `create_all` used.
- [ ] App is deployed and the live link works (smoke tested).
- [ ] Demo video recorded (2–4 min) and linked in README.
- [ ] Repo link sent by replying to the same email.

# ACME Salary Management — Artifacts

> Documents the thinking, decisions, and approach behind the solution.
> Updated as the build progresses.

---

## Key Design Decisions

**1. Postgres everywhere**
Single DB engine across local and production. Eliminates dialect differences, and gives us native `percentile_cont` for median salary — no Python workaround needed.

**2. Salary as integer**
Annual salary stored as a whole-number integer in local currency (e.g. 75000 = £75,000). Avoids float rounding bugs. HR always works in whole units.

**3. Local currency + fixed conversion table**
Each employee's salary stays in their local currency. A `currency_rates` table (fixed as of 2024-01-01) handles USD conversion for cross-country comparisons on the Insights page. Keeps local context intact without an external API dependency.

**4. Alembic migrations**
Versioned, sequential migration files (`001_create_employees.py`, `002_...`) instead of `create_all`. Every schema change is reviewable, reversible, and traceable.

**5. Server-side pagination**
The API never returns all 10,000 rows. Page + page_size (max 100), with server-side filtering and sorting. The `sort_by` field is validated against an allow-list to prevent injection.

**6. Layered backend**
Routes → Services → Repositories. Business rules live only in services, making them testable without HTTP. Repositories are the only place that touches the DB.

---

## Trade-offs

| Decision | Why |
|---|---|
| No authentication | Single user (HR Manager). Adds complexity with no assessment value. Listed as next step. |
| Fixed currency rates | Deterministic and testable. Live rates need an external service and introduce flakiness. |
| No salary history | Adds schema complexity. Out of scope for this iteration. |
| `create_all` skipped for Alembic | More overhead upfront, but production-ready and traceable from day one. |
| Distribution buckets server-computed | Keeps the frontend simple. 10 fixed USD buckets, consistent across all filters. |

---

## AI Usage Log

| # | Prompt | AI produced | What I changed |
|---|---|---|---|
| 1 | Review plan against assessment requirements | Gap analysis — 1 critical, 5 medium, 4 low findings | Accepted all; locked deployment decision upfront |
| 2 | Fix the gaps | Updated plan with deployment, meta/filters tests, demo task, AI log | Chose Postgres everywhere over SQLite/Postgres split |
| 3 | Use Postgres + pgAdmin locally | Updated plan and artifacts | Confirmed; removed all SQLite references |
| 4 | Use Alembic not create_all | Generated alembic config, migration file, updated database.py | Fixed psycopg2 dialect issue; wrote migration manually |
| 5 | Sequential migration naming | Configured `file_template`, renamed migration, MSG guard in Makefile | Confirmed |

---

## Performance Considerations

- **Indexes** on `country_code`, `job_title`, `department`, `last_name`, and composite `(country_code, job_title)`
- **Search** uses `LIKE '%term%'` — no index benefit, acceptable at 10k rows. Upgrade path: `pg_trgm`
- **Seed** uses bulk insert in batches of 500, not row-by-row. Target: under 10 seconds for 10,000 rows
- **Insights** run as single aggregation queries per endpoint — no app-level loops over rows
- Actual measured timings will be added after deployment

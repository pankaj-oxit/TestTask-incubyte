# Run all commands from the repository root.

BACKEND = backend
PYTHON  = $(BACKEND)/.venv/bin/python
ALEMBIC = $(BACKEND)/.venv/bin/alembic
PYTEST  = $(BACKEND)/.venv/bin/pytest

.PHONY: help up down db-up env migrate run seed test ui explain \
        migrate-new migrate-down migrate-status

help:
	@echo "Docker (repo root):"
	@echo "  make up      Start db + API + UI (compose up --build)"
	@echo "  make down    Stop compose stack"
	@echo "  make db-up   Postgres only (background)"
	@echo ""
	@echo "Host backend (needs backend/.venv — see README):"
	@echo "  make env     Create backend/.env from .env.example"
	@echo "  make migrate Apply Alembic migrations"
	@echo "  make run     Uvicorn with reload on :8000"
	@echo "  make seed    Insert 10k employees (skip if rows exist)"
	@echo ""
	@echo "Host frontend:"
	@echo "  make ui      Vite dev server on :5173"
	@echo ""
	@echo "  make test    Backend pytest + frontend vitest"
	@echo "  make explain Postgres EXPLAIN for list/insights queries (needs DATABASE_URL)"

up:
	docker compose up --build

down:
	docker compose down

db-up:
	docker compose up db -d

env:
	@test -f $(BACKEND)/.env || cp $(BACKEND)/.env.example $(BACKEND)/.env
	@echo "Created $(BACKEND)/.env (localhost Postgres)."

migrate: env
	cd $(BACKEND) && $(ALEMBIC) upgrade head

run: env
	cd $(BACKEND) && $(PYTHON) -m uvicorn app.main:app --reload

seed: env
	cd $(BACKEND) && $(PYTHON) scripts/seed.py

test:
	cd $(BACKEND) && $(PYTEST) -q
	cd frontend && npm test

explain: env
	cd $(BACKEND) && $(PYTHON) scripts/explain_queries.py

ui:
	cd frontend && npm run dev

migrate-new:
	@test -n "$(MSG)" || (echo 'Usage: make migrate-new MSG=003_description' && exit 1)
	cd $(BACKEND) && $(ALEMBIC) revision -m "$(MSG)"

migrate-down:
	cd $(BACKEND) && $(ALEMBIC) downgrade -1

migrate-status:
	cd $(BACKEND) && $(ALEMBIC) current

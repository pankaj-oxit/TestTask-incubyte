PYTHON  = .venv/bin/python
ALEMBIC = .venv/bin/alembic
PYTEST  = .venv/bin/pytest

.PHONY: env migrate migrate-new migrate-down migrate-status run seed test

env:
	@test -f .env || cp .env.example .env
	@echo "Created backend/.env (localhost Postgres). Edit if your credentials differ."

.env:
	@test -f .env || (echo "Missing backend/.env — run: make env" && exit 1)

migrate: .env
	$(ALEMBIC) upgrade head

migrate-new:
	@test -n "$(MSG)" || (echo 'Usage: make migrate-new MSG=003_description' && exit 1)
	$(ALEMBIC) revision -m "$(MSG)"

migrate-down:
	$(ALEMBIC) downgrade -1

migrate-status:
	$(ALEMBIC) current

run: .env
	$(PYTHON) -m uvicorn app.main:app --reload

seed: .env
	$(PYTHON) scripts/seed.py

test:
	$(PYTEST)

# Convenience commands — run from backend/ directory
# Requires virtualenv: python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"

PYTHON  = .venv/bin/python
ALEMBIC = .venv/bin/alembic
PYTEST  = .venv/bin/pytest

.PHONY: migrate migrate-new migrate-down migrate-status run seed test

## Apply all pending migrations to the database
migrate:
	$(ALEMBIC) upgrade head

## Create a new versioned migration file.
##
## Usage:  make migrate-new MSG=002_add_department_index
##
## MSG is a variable you pass on the command line — it becomes the filename and
## the description inside the migration file.  Follow the naming convention:
##   NNN_verb_table_or_feature   e.g.  003_add_hire_date_index
##
## The file will be created at: migrations/versions/<MSG>.py
## After creation, open it and fill in the upgrade() / downgrade() functions.
migrate-new:
ifndef MSG
	$(error MSG is required. Usage: make migrate-new MSG=002_add_department_index)
endif
	$(ALEMBIC) revision -m "$(MSG)"

## Roll back the most recently applied migration
migrate-down:
	$(ALEMBIC) downgrade -1

## Show which migration is currently applied
migrate-status:
	$(ALEMBIC) current

## Show full migration history
migrate-history:
	$(ALEMBIC) history --verbose

## Start the development server (auto-reload)
run:
	$(PYTHON) -m uvicorn app.main:app --reload

## Seed the database with 10,000 employees
seed:
	$(PYTHON) scripts/seed.py

## Run all tests with coverage report
test:
	$(PYTEST)

.PHONY: up down db-up test

up:
	docker compose up --build

db-up:
	docker compose up db -d

down:
	docker compose down

test:
	cd backend && .venv/bin/pytest -q

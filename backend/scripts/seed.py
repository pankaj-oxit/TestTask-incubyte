"""Seed employees: deterministic bulk insert (default 10,000)."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

# Allow running as `python scripts/seed.py` from backend/
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy.exc import OperationalError

from app.database import SessionLocal
from app.services.seed_service import DEFAULT_COUNT, seed_employees


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed ACME employee data")
    parser.add_argument("--reset", action="store_true", help="Delete existing employees first")
    parser.add_argument("--count", type=int, default=DEFAULT_COUNT, help="Number of rows to insert")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        started = time.perf_counter()
        inserted = seed_employees(db, count=args.count, reset=args.reset)
        elapsed = time.perf_counter() - started
        if inserted:
            print(f"Seeded {inserted} employees in {elapsed:.2f}s")
        else:
            print("Skipped seed — employees already present (use --reset to replace)")
    except OperationalError as exc:
        print(
            "Database connection failed. Start Postgres first:\n"
            "  from repo root: make db-up   (then: make migrate)\n"
            "  or full stack: make up",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc
    finally:
        db.close()


if __name__ == "__main__":
    main()

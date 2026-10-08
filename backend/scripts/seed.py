"""Seed 10,000 deterministic employees (Phase 4). Currency rates come from Alembic migration 002."""

import sys


def main() -> None:
    print(
        "Employee seed is planned for Phase 4 (10,000 rows via Faker + bulk insert). "
        "Run: make migrate  then  make seed  once implemented.",
        file=sys.stderr,
    )
    sys.exit(1)


if __name__ == "__main__":
    main()

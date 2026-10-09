#!/usr/bin/env python3
"""Print EXPLAIN plans for common list/insights SQL (Postgres). Run from repo: make explain."""

from __future__ import annotations

import os
import sys
import time

from sqlalchemy import create_engine, text

QUERIES: list[tuple[str, str]] = [
    (
        "list_page_country_sort",
        """
        EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
        SELECT * FROM employees
        WHERE country_code = 'US'
        ORDER BY last_name ASC
        LIMIT 25 OFFSET 0
        """,
    ),
    (
        "list_search_like",
        """
        EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
        SELECT * FROM employees
        WHERE lower(first_name) LIKE '%john%' OR lower(last_name) LIKE '%john%' OR lower(email) LIKE '%john%'
        ORDER BY last_name ASC
        LIMIT 25 OFFSET 0
        """,
    ),
    (
        "insights_by_country",
        """
        EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
        SELECT country_code, COUNT(*), AVG(annual_salary)
        FROM employees
        GROUP BY country_code
        ORDER BY country_code
        """,
    ),
]


def main() -> int:
    url = os.environ.get("DATABASE_URL")
    if not url:
        print("DATABASE_URL not set", file=sys.stderr)
        return 1
    if "sqlite" in url.lower():
        print("EXPLAIN script requires Postgres (DATABASE_URL)", file=sys.stderr)
        return 1

    engine = create_engine(url)
    with engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM employees")).scalar_one()
        print(f"employees row count: {count}\n")

        for name, sql in QUERIES:
            print(f"=== {name} ===")
            t0 = time.perf_counter()
            rows = conn.execute(text(sql)).all()
            elapsed_ms = (time.perf_counter() - t0) * 1000
            for row in rows:
                print(row[0])
            print(f"(client elapsed {elapsed_ms:.1f} ms)\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

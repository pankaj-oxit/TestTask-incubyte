"""Deterministic employee seed (bulk insert, idempotent)."""

from __future__ import annotations

import random
from datetime import date, timedelta

from faker import Faker
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.services.currency_service import COUNTRY_CURRENCY_MAP

DEFAULT_SEED = 42
DEFAULT_COUNT = 10_000
BATCH_SIZE = 500

JOB_TITLES = [
    "Software Engineer",
    "Senior Software Engineer",
    "Engineering Manager",
    "Product Manager",
    "Data Analyst",
    "HR Business Partner",
    "Sales Representative",
    "Account Executive",
    "Customer Success Manager",
    "Finance Analyst",
]

DEPARTMENTS = [
    "Engineering",
    "Product",
    "Sales",
    "Customer Success",
    "Human Resources",
    "Finance",
    "Operations",
]

# Annual salary range in local currency (min, max), whole units
COUNTRY_SALARY_BANDS: dict[str, tuple[int, int]] = {
    "US": (55_000, 185_000),
    "IN": (600_000, 3_500_000),
    "GB": (32_000, 95_000),
    "DE": (45_000, 110_000),
    "FR": (42_000, 105_000),
    "CA": (50_000, 130_000),
    "AU": (65_000, 145_000),
    "SG": (48_000, 120_000),
    "JP": (4_500_000, 12_000_000),
    "BR": (60_000, 220_000),
}

COUNTRY_CODES = list(COUNTRY_CURRENCY_MAP.keys())


def generate_employee_rows(count: int, *, seed: int = DEFAULT_SEED) -> list[dict]:
    rng = random.Random(seed)
    fake = Faker()
    Faker.seed(seed)
    today = date.today()
    earliest_hire = today - timedelta(days=15 * 365)
    rows: list[dict] = []

    for i in range(count):
        country_code = COUNTRY_CODES[i % len(COUNTRY_CODES)]
        currency = COUNTRY_CURRENCY_MAP[country_code]
        sal_min, sal_max = COUNTRY_SALARY_BANDS[country_code]
        annual_salary = rng.randint(sal_min, sal_max)
        hire_offset = rng.randint(0, (today - earliest_hire).days)
        hire_date = earliest_hire + timedelta(days=hire_offset)
        first_name = fake.first_name()
        last_name = fake.last_name()
        rows.append(
            {
                "employee_code": f"EMP-{i + 1:06d}",
                "first_name": first_name,
                "last_name": last_name,
                "email": f"employee{i + 1:06d}@acme.example",
                "job_title": JOB_TITLES[rng.randint(0, len(JOB_TITLES) - 1)],
                "department": DEPARTMENTS[rng.randint(0, len(DEPARTMENTS) - 1)],
                "country_code": country_code,
                "currency": currency,
                "annual_salary": annual_salary,
                "hire_date": hire_date,
            }
        )
    return rows


def seed_employees(db: Session, count: int = DEFAULT_COUNT, *, reset: bool = False) -> int:
    existing = db.query(Employee).count()
    if existing > 0 and not reset:
        return 0
    if reset and existing > 0:
        db.query(Employee).delete()
        db.commit()

    rows = generate_employee_rows(count)
    for start in range(0, len(rows), BATCH_SIZE):
        batch = rows[start : start + BATCH_SIZE]
        db.bulk_insert_mappings(Employee, batch)
        db.commit()
    return len(rows)

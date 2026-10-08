from datetime import date

from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.services.seed_service import DEFAULT_SEED, generate_employee_rows, seed_employees


def test_generate_rows_deterministic():
    a = generate_employee_rows(50, seed=DEFAULT_SEED)
    b = generate_employee_rows(50, seed=DEFAULT_SEED)
    assert a == b
    assert len(a) == 50
    emails = [r["email"] for r in a]
    assert len(emails) == len(set(emails))


def test_seed_skips_when_data_exists(db: Session):
    db.add(
        Employee(
            employee_code="EMP-EXIST",
            first_name="A",
            last_name="B",
            email="exist@acme.com",
            job_title="Engineer",
            department="Engineering",
            country_code="US",
            currency="USD",
            annual_salary=80000,
            hire_date=date(2019, 6, 1),
        )
    )
    db.commit()
    inserted = seed_employees(db, count=10, reset=False)
    assert inserted == 0
    assert db.query(Employee).count() == 1


def test_seed_reset_and_insert(db: Session):
    db.add(
        Employee(
            employee_code="EMP-OLD",
            first_name="Old",
            last_name="User",
            email="old@acme.com",
            job_title="Engineer",
            department="Engineering",
            country_code="US",
            currency="USD",
            annual_salary=70000,
            hire_date=date(2018, 1, 1),
        )
    )
    db.commit()
    inserted = seed_employees(db, count=200, reset=True)
    assert inserted == 200
    assert db.query(Employee).count() == 200

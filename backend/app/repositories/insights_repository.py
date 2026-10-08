from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.employee import Employee


class InsightsRepository:
    def __init__(self, db: Session):
        self._db = db

    def list_salary_rows(
        self,
        *,
        country_code: str | None = None,
        job_title: str | None = None,
    ) -> list[tuple[str, str, str, int]]:
        query = select(
            Employee.country_code,
            Employee.job_title,
            Employee.currency,
            Employee.annual_salary,
        )
        if country_code:
            query = query.where(Employee.country_code == country_code)
        if job_title:
            query = query.where(Employee.job_title == job_title)
        return list(self._db.execute(query).all())

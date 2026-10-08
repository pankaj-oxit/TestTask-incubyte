from sqlalchemy import asc, desc, func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeListParams, EmployeeUpdate


class EmployeeRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_by_id(self, employee_id: int) -> Employee | None:
        return self._db.get(Employee, employee_id)

    def create(self, data: EmployeeCreate) -> Employee:
        employee = Employee(**data.model_dump())
        self._db.add(employee)
        try:
            self._db.commit()
        except IntegrityError:
            self._db.rollback()
            raise
        self._db.refresh(employee)
        return employee

    def update(self, employee: Employee, data: EmployeeUpdate) -> Employee:
        for key, value in data.model_dump().items():
            setattr(employee, key, value)
        try:
            self._db.commit()
        except IntegrityError:
            self._db.rollback()
            raise
        self._db.refresh(employee)
        return employee

    def delete(self, employee: Employee) -> None:
        self._db.delete(employee)
        self._db.commit()

    def list_employees(self, params: EmployeeListParams) -> tuple[list[Employee], int]:
        query = select(Employee)
        query = self._apply_filters(query, params)
        count_query = select(func.count()).select_from(query.subquery())
        total = self._db.scalar(count_query) or 0

        sort_column = getattr(Employee, params.sort_by)
        ordering = asc(sort_column) if params.order == "asc" else desc(sort_column)
        query = query.order_by(ordering)
        offset = (params.page - 1) * params.page_size
        rows = self._db.scalars(query.offset(offset).limit(params.page_size)).all()
        return list(rows), total

    def distinct_filter_values(self) -> dict[str, list[str]]:
        countries = self._db.scalars(
            select(Employee.country_code).distinct().order_by(Employee.country_code)
        ).all()
        departments = self._db.scalars(
            select(Employee.department).distinct().order_by(Employee.department)
        ).all()
        job_titles = self._db.scalars(
            select(Employee.job_title).distinct().order_by(Employee.job_title)
        ).all()
        return {
            "countries": list(countries),
            "departments": list(departments),
            "job_titles": list(job_titles),
        }

    @staticmethod
    def _apply_filters(query, params: EmployeeListParams):
        if params.country:
            query = query.where(Employee.country_code == params.country)
        if params.job_title:
            query = query.where(Employee.job_title == params.job_title)
        if params.department:
            query = query.where(Employee.department == params.department)
        if params.search:
            term = f"%{params.search.lower()}%"
            query = query.where(
                or_(
                    func.lower(Employee.first_name).like(term),
                    func.lower(Employee.last_name).like(term),
                    func.lower(Employee.email).like(term),
                )
            )
        return query

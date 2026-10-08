from sqlalchemy.exc import IntegrityError

from app.core.errors import ConflictError, NotFoundError
from app.models.employee import Employee
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeListParams, EmployeeUpdate


class EmployeeService:
    def __init__(self, repo: EmployeeRepository):
        self._repo = repo

    def create(self, data: EmployeeCreate) -> Employee:
        try:
            return self._repo.create(data)
        except IntegrityError as exc:
            raise ConflictError("Employee with this email or employee code already exists") from exc

    def get(self, employee_id: int) -> Employee:
        employee = self._repo.get_by_id(employee_id)
        if employee is None:
            raise NotFoundError("Employee", employee_id)
        return employee

    def update(self, employee_id: int, data: EmployeeUpdate) -> Employee:
        employee = self.get(employee_id)
        try:
            return self._repo.update(employee, data)
        except IntegrityError as exc:
            raise ConflictError("Employee with this email or employee code already exists") from exc

    def delete(self, employee_id: int) -> None:
        employee = self.get(employee_id)
        self._repo.delete(employee)

    def list_employees(self, params: EmployeeListParams) -> tuple[list[Employee], int]:
        return self._repo.list_employees(params)

    def filter_options(self) -> dict[str, list[str]]:
        return self._repo.distinct_filter_values()

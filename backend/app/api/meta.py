from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.employee import Employee
from app.repositories.employee_repository import EmployeeRepository
from app.services.employee_service import EmployeeService

meta_router = APIRouter(prefix="/meta", tags=["meta"])
health_router = APIRouter(tags=["meta"])


def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:
    return EmployeeService(EmployeeRepository(db))


@meta_router.get("/filters")
def meta_filters(service: EmployeeService = Depends(get_employee_service)) -> dict[str, list[str]]:
    return service.filter_options()


@health_router.get("/health")
def health_check(db: Session = Depends(get_db)) -> dict:
    """Returns service status and current employee count."""
    employee_count = db.query(Employee).count()
    return {"status": "ok", "employee_count": employee_count}

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeListParams,
    EmployeeListResponse,
    EmployeeResponse,
    EmployeeUpdate,
)
from app.services.employee_service import EmployeeService

router = APIRouter(prefix="/employees", tags=["employees"])


def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:
    return EmployeeService(EmployeeRepository(db))


@router.get("", response_model=EmployeeListResponse)
def list_employees(
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    search: str | None = None,
    country: str | None = None,
    job_title: str | None = None,
    department: str | None = None,
    sort_by: str = "last_name",
    order: str = "asc",
    service: EmployeeService = Depends(get_employee_service),
) -> EmployeeListResponse:
    params = EmployeeListParams(
        page=page,
        page_size=page_size,
        search=search,
        country=country,
        job_title=job_title,
        department=department,
        sort_by=sort_by,
        order=order,  # type: ignore[arg-type]
    )
    items, total = service.list_employees(params)
    return EmployeeListResponse(
        items=[EmployeeResponse.model_validate(e) for e in items],
        total=total,
        page=params.page,
        page_size=params.page_size,
    )


@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    payload: EmployeeCreate,
    service: EmployeeService = Depends(get_employee_service),
) -> EmployeeResponse:
    employee = service.create(payload)
    return EmployeeResponse.model_validate(employee)


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    service: EmployeeService = Depends(get_employee_service),
) -> EmployeeResponse:
    employee = service.get(employee_id)
    return EmployeeResponse.model_validate(employee)


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    payload: EmployeeUpdate,
    service: EmployeeService = Depends(get_employee_service),
) -> EmployeeResponse:
    employee = service.update(employee_id, payload)
    return EmployeeResponse.model_validate(employee)


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    service: EmployeeService = Depends(get_employee_service),
) -> Response:
    service.delete(employee_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

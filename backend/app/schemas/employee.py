from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator

from app.services.currency_service import validate_currency_for_country

SORTABLE_FIELDS = frozenset(
    {
        "employee_code",
        "first_name",
        "last_name",
        "email",
        "job_title",
        "department",
        "country_code",
        "annual_salary",
        "hire_date",
    }
)


class EmployeeBase(BaseModel):
    employee_code: str = Field(..., min_length=1, max_length=20)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    job_title: str = Field(..., min_length=1, max_length=100)
    department: str = Field(..., min_length=1, max_length=100)
    country_code: str = Field(..., min_length=2, max_length=2)
    currency: str = Field(..., min_length=3, max_length=3)
    annual_salary: int = Field(..., gt=0)
    hire_date: date

    @field_validator("hire_date")
    @classmethod
    def hire_date_not_future(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("hire_date cannot be in the future")
        return value

    @model_validator(mode="after")
    def currency_matches_country(self) -> "EmployeeBase":
        try:
            validate_currency_for_country(self.country_code, self.currency)
        except ValueError as exc:
            raise ValueError(str(exc)) from exc
        return self


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class EmployeeResponse(EmployeeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class EmployeeListResponse(BaseModel):
    items: list[EmployeeResponse]
    total: int
    page: int
    page_size: int


class EmployeeListParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(25, ge=1, le=100)
    search: str | None = None
    country: str | None = None
    job_title: str | None = None
    department: str | None = None
    sort_by: str = "last_name"
    order: Literal["asc", "desc"] = "asc"

    @field_validator("sort_by")
    @classmethod
    def sort_by_allowed(cls, value: str) -> str:
        if value not in SORTABLE_FIELDS:
            raise ValueError(f"sort_by must be one of: {', '.join(sorted(SORTABLE_FIELDS))}")
        return value

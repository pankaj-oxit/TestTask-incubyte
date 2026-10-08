from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.core.errors import (
    AppValidationError,
    ConflictError,
    NotFoundError,
    conflict_handler,
    not_found_handler,
    validation_error_handler,
)
from app.api import employees, insights, meta
from app.config import settings
from app.database import SessionLocal
from app.services.seed_service import DEFAULT_COUNT, seed_employees

api_router = APIRouter(prefix="/api")
api_router.include_router(meta.health_router)
api_router.include_router(meta.meta_router)
api_router.include_router(employees.router)
api_router.include_router(insights.router)

app = FastAPI(
    title="ACME Salary Manager",
    description="HR salary management API for 10,000 employees across multiple countries.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def _validation_message(exc: RequestValidationError | ValidationError) -> str:
    if not exc.errors():
        return "Validation error"
    err = exc.errors()[0]
    if err.get("type") == "value_error":
        return str(err.get("ctx", {}).get("error") or err["msg"])
    return str(err["msg"])


async def request_validation_handler(_request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": _validation_message(exc), "code": "VALIDATION_ERROR"},
    )


async def pydantic_validation_handler(_request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": _validation_message(exc), "code": "VALIDATION_ERROR"},
    )


app.add_exception_handler(RequestValidationError, request_validation_handler)
app.add_exception_handler(ValidationError, pydantic_validation_handler)
app.add_exception_handler(NotFoundError, not_found_handler)
app.add_exception_handler(ConflictError, conflict_handler)
app.add_exception_handler(AppValidationError, validation_error_handler)

app.include_router(api_router)


@app.on_event("startup")
def seed_on_startup_if_empty() -> None:
    if not settings.auto_seed_on_startup:
        return
    db = SessionLocal()
    try:
        seed_employees(db, count=DEFAULT_COUNT, reset=False)
    finally:
        db.close()

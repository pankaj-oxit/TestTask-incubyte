from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.core.errors import (
    AppValidationError,
    ConflictError,
    NotFoundError,
    conflict_handler,
    not_found_handler,
    validation_error_handler,
)
from app.api import meta

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

app.add_exception_handler(NotFoundError, not_found_handler)
app.add_exception_handler(ConflictError, conflict_handler)
app.add_exception_handler(AppValidationError, validation_error_handler)

app.include_router(meta.router, tags=["meta"])

from fastapi import Request
from fastapi.responses import JSONResponse


class NotFoundError(Exception):
    def __init__(self, resource: str, identifier: str | int):
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} '{identifier}' not found")


class ConflictError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class AppValidationError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc), "code": "NOT_FOUND"})


async def conflict_handler(request: Request, exc: ConflictError) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": exc.message, "code": "CONFLICT"})


async def validation_error_handler(request: Request, exc: AppValidationError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": exc.message, "code": "VALIDATION_ERROR"})

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


class BaseInternalException(Exception):
    """
    Base error class for inherit all internal errors.
    """

    _status_code = 0
    _message = ""

    def __init__(
        self,
        status_code: int | None = None,
        message: str | None = None,
        errors: list[str] | None = None,
    ) -> None:
        self.status_code = status_code
        self.message = message
        self.errors = errors

    def get_status_code(self) -> int:
        return self.status_code or self._status_code

    def get_message(self) -> str:
        return self.message or self._message

    @classmethod
    def get_response(cls) -> JSONResponse:
        return JSONResponse(
            status_code=cls._status_code,
            content={
                "status": "error",
                "status_code": cls._status_code,
                "type": cls.__name__,
                "message": cls._message,
            },
        )


class ThreadNotFoundException(BaseInternalException):
    """Exception raised when article not found in database."""

    _status_code = 404
    _message = "Thread with this slug does not exist."


class ThreadPermissionException(BaseInternalException):
    """Exception raised when user does not have permission to access the article."""

    _status_code = 403
    _message = "Current user does not have permission to access the article."


def add_internal_exception_handler(app: FastAPI) -> None:
    """
    Handle all internal exceptions.
    """

    @app.exception_handler(BaseInternalException)
    async def _exception_handler(
        _: Request, exc: BaseInternalException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.get_status_code(),
            content={
                "status": "error",
                "status_code": exc.get_status_code(),
                "type": type(exc).__name__,
                "message": exc.get_message(),
            },
        )


def add_request_exception_handler(app: FastAPI) -> None:
    """
    Handle request validation errors exceptions.
    """

    @app.exception_handler(RequestValidationError)
    async def _exception_handler(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "status": "error",
                "status_code": 422,
                "type": "RequestValidationError",
                "message": "Schema validation error",
                "errors": exc.errors(),
            },
        )


def add_http_exception_handler(app: FastAPI) -> None:
    """
    Handle http exceptions.
    """

    @app.exception_handler(HTTPException)
    async def _exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "status_code": exc.status_code,
                "type": "HTTPException",
                "message": exc.detail,
            },
        )


def add_exception_handlers(app: FastAPI) -> None:
    """
    Set all exception handlers to app object.
    """
    add_internal_exception_handler(app=app)
    add_request_exception_handler(app=app)
    add_http_exception_handler(app=app)

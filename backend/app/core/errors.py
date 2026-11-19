import logging
from typing import Any

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

ERROR_CODES = {
    400: "BAD_REQUEST",
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    405: "METHOD_NOT_ALLOWED",
    409: "CONFLICT",
    422: "VALIDATION_ERROR",
}


class AppError(Exception):
    """Erro de aplicação com resposta padronizada e segura ao cliente."""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        fields: dict[str, Any] | None = None,
    ) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        self.fields = fields
        super().__init__(message)


def error_response(
    status_code: int,
    code: str,
    message: str,
    fields: dict[str, Any] | None = None,
) -> JSONResponse:
    detail: dict[str, Any] = {"code": code, "message": message}
    if fields:
        detail["fields"] = fields
    return JSONResponse(status_code=status_code, content={"detail": detail})


async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return error_response(exc.status_code, exc.code, exc.message, exc.fields)


async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    code = ERROR_CODES.get(exc.status_code, "HTTP_ERROR")
    message = exc.detail if isinstance(exc.detail, str) else "Não foi possível concluir a operação."
    return error_response(exc.status_code, code, message)


async def request_validation_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    fields: dict[str, str] = {}
    for error in exc.errors():
        location = [str(part) for part in error["loc"] if part not in {"body", "query", "path"}]
        fields[".".join(location) or "detail"] = str(error["msg"])
    return error_response(422, "VALIDATION_ERROR", "Verifique os campos destacados.", fields)


async def unexpected_error_handler(request: Request, _: Exception) -> JSONResponse:
    logger.exception("Erro não tratado em %s", request.url.path)
    return error_response(500, "INTERNAL_ERROR", "Não foi possível concluir a operação.")


def register_error_handlers(app: Any) -> None:
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_handler)
    app.add_exception_handler(Exception, unexpected_error_handler)

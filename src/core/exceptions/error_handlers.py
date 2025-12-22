"""Error handlers for FastAPI application."""

import logging
from typing import Any

from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from core.exceptions.base_exception import BaseAppException

logger = logging.getLogger(__name__)


def base_app_exception_handler(
    request: Request,
    exc: BaseAppException,
) -> JSONResponse:
    """Handle custom application exceptions."""
    logger.error(
        f"Application error: {exc.message}",
        extra={"status_code": exc.status_code, "detail": exc.detail},
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.message,
            "detail": exc.detail,
        },
    )


def sqlalchemy_exception_handler(
    request: Request, exc: SQLAlchemyError
) -> JSONResponse:
    """Handle SQLAlchemy database exceptions."""
    logger.error(f"Database error: {str(exc)}", exc_info=True)

    if isinstance(exc, IntegrityError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": True,
                "message": "Database integrity error",
                "detail": "A database constraint violation occurred",
            },
        )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "Database error",
            "detail": "An error occurred while accessing the database",
        },
    )


def general_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.error(
        f"Unexpected error: {str(exc)}",
        exc_info=True,
        extra={"path": request.url.path, "method": request.method},
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "Internal server error",
            "detail": "An unexpected error occurred",
        },
    )


def register_error_handlers(app: Any) -> None:
    """Register all error handlers to the FastAPI app."""
    app.add_exception_handler(BaseAppException, base_app_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

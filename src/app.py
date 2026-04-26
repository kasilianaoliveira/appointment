from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from core.exceptions.error_handlers import register_error_handlers
from core.logging_config import setup_logging
from core.settings import get_settings
from routers.admin_daily_limit_router import protected_admin_daily_router
from routers.appointments_router import (
    protected_admin_router as appointments_admin_router,
)
from routers.appointments_router import (
    protected_user_router as appointments_user_router,
)
from routers.auth_router import auth_public_router
from routers.services_router import public_services_router, services_router
from routers.user_router import protected_user_router, user_public_router

setup_logging()

config = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Appointment",
        description="API for appointment services",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[config.FRONTEND_ORIGIN],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        SessionMiddleware,  # ty:ignore[invalid-argument-type]
        secret_key=config.SECRET_KEY.get_secret_value(),
    )

    app.include_router(user_public_router)
    app.include_router(protected_user_router)

    app.include_router(auth_public_router)

    app.include_router(public_services_router)
    app.include_router(services_router)

    app.include_router(appointments_user_router)
    app.include_router(appointments_admin_router)

    app.include_router(protected_admin_daily_router)
    # app.include_router(storage_router)

    register_error_handlers(app)

    return app


app_fast = create_app()
add_pagination(app_fast)

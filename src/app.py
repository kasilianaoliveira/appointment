from fastapi import FastAPI
from fastapi_pagination import add_pagination

from core.exceptions.error_handlers import register_error_handlers
from core.logging_config import setup_logging
from routers.appointments_router import (
    protected_admin_router as appointments_admin_router,
    protected_user_router as appointments_user_router,
)
from routers.services_router import public_services_router, services_router
from routers.user_router import protected_user_router, user_public_router

setup_logging()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Appointment",
        description="API for appointment services",
    )
    app.include_router(user_public_router)
    app.include_router(protected_user_router)

    app.include_router(public_services_router)
    app.include_router(services_router)

    app.include_router(appointments_user_router)
    app.include_router(appointments_admin_router)

    register_error_handlers(app)

    return app


app = create_app()
add_pagination(app)

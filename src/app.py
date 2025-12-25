from fastapi import FastAPI
from fastapi_pagination import add_pagination

from core.exceptions.error_handlers import register_error_handlers
from core.logging_config import setup_logging
from routers.services_router import services_router
from routers.user_router import protected_user_router, user_public_router

setup_logging()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Appointment",
        description="API for appointment services",
    )
    app.include_router(user_public_router)
    app.include_router(protected_user_router)
    app.include_router(services_router)

    register_error_handlers(app)

    return app


app = create_app()
add_pagination(app)

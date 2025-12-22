from fastapi import FastAPI
from fastapi_pagination import add_pagination

from core.logging_config import setup_logging
from routers.user_router import router

setup_logging()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Appointment",
        description="API for appointment services",
    )
    app.include_router(router)

    return app


app = create_app()
add_pagination(app)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from amichan.api.router import router
from amichan.core.config import get_app_settings


def create_app() -> FastAPI:
    settings = get_app_settings()

    application = FastAPI(**settings.fastapi_kwargs)
    application.include_router(router)
    application.mount(
        "/", StaticFiles(directory="frontend/dist", html=True), name="static"
    )

    return application


app = create_app()

from fastapi import FastAPI

from amichan.api.router import router
from amichan.core.config import get_app_settings


def create_app() -> FastAPI:
    settings = get_app_settings()

    # print("JWT Secret Key:", settings.jwt_secret_key)

    application = FastAPI(**settings.fastapi_kwargs)
    application.include_router(router)

    return application


app = create_app()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from amichan.api.router import router
from amichan.core.config import get_app_settings


def create_app() -> FastAPI:
    settings = get_app_settings()

    application = FastAPI(**settings.fastapi_kwargs)
    application.include_router(router)
    # application.mount(
    #     "/", StaticFiles(directory="frontend/dist", html=True), name="static"
    # )

    origins = [
        "http://localhost:5173",  # Для фронтенда на Vite
        "http://127.0.0.1:5173",
    ]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # Разрешенные источники
        allow_credentials=True,
        allow_methods=["*"],  # Разрешенные методы (GET, POST и т.д.)
        allow_headers=["*"],  # Разрешенные заголовки
    )

    return application


app = create_app()

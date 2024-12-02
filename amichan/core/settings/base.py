from pydantic import computed_field
from pydantic_settings import BaseSettings
from sqlalchemy import URL


class BaseAppSettings(BaseSettings):
    """
    Base application setting class.
    """

    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str
    database_url: str

    class Config:
        env_file = ".env"

    # jwt_secret_key: str
    # jwt_token_expiration_minutes: int = 60 * 24 * 7  # one week.
    # jwt_algorithm: str = "HS256"

    @computed_field  # type: ignore
    @property
    def sql_db_uri(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        )

    @computed_field  # type: ignore
    @property
    def sqlalchemy_engine_props(self) -> dict:
        return dict(url=self.sql_db_uri)

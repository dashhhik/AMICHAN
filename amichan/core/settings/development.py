import logging

from pydantic import computed_field

from amichan.core.settings.app import AppSettings


class DevAppSettings(AppSettings):
    """
    Development application settings.
    """

    debug: bool = True

    title: str = "[DEV] Amichan API"

    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".env"

    @computed_field  # type: ignore
    @property
    def sqlalchemy_engine_props(self) -> dict:
        return dict(url=self.sql_db_uri, echo=True)

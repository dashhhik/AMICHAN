import logging

from pydantic import computed_field

from amichan.core.settings.app import AppSettings


class DevAppSettings(AppSettings):
    """
    Development application settings.
    """

    debug: bool = True
    mail_username: str
    mail_from: str
    mail_port: int
    mail_server: str
    mail_tls: bool
    mail_ssl: bool
    use_credentials: bool = True

    title: str = "[DEV] Amichan API"

    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".env"
        extra = "allow"

    @computed_field  # type: ignore
    @property
    def sqlalchemy_engine_props(self) -> dict:
        return dict(url=self.sql_db_uri, echo=True)

from functools import lru_cache

from amichan.core.settings.app import AppSettings
from amichan.core.settings.development import DevAppSettings


@lru_cache
def get_app_settings() -> AppSettings:
    """
    Return application config.
    """

    return DevAppSettings()

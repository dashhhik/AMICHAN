import abc
from datetime import timedelta
from typing import Any

from amichan.domain.dtos.user import UserDTO


class IJWTService(abc.ABC):
    """Interface for UserAuth service."""

    @abc.abstractmethod
    async def generate(self, email: str, role_id: int, exp: timedelta) -> str: ...

    @abc.abstractmethod
    async def parse(self, token: str) -> UserDTO|None: ...

    @abc.abstractmethod
    async def ban_user(
        self, session: Any, email: str, reason: str, duration: int
    ) -> None: ...

    @abc.abstractmethod
    async def login(
            self, session: Any, email: str, password: str
    ) -> UserDTO | None: ...
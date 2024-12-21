import abc
from datetime import timedelta

from amichan.domain.dtos.user import UserDTO


class IJWTService(abc.ABC):
    """Interface for UserAuth service."""

    @abc.abstractmethod
    async def generate(self, email: str, role_id: int, exp: timedelta) -> str: ...

    @abc.abstractmethod
    async def parse(self, token: str) -> UserDTO: ...

    @abc.abstractmethod
    async def ban_user(self, email: str, reason: str, duration: int) -> None: ...

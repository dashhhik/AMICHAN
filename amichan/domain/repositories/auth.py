import abc
from typing import Any


class IAuthRepository(abc.ABC):
    @abc.abstractmethod
    async def ban_user(
        self, session: Any, email: str, reason: str, duration: int
    ) -> None: ...

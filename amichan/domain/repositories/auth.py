import abc
from typing import Any


class IAuthRepository(abc.ABC):
    @abc.abstractmethod
    async def ban_user(
        self, session: Any, email: str, reason: str, duration: int
    ) -> None: ...

    @abc.abstractmethod
    async def login(self, session: Any, email:str, password:str) -> int: ...

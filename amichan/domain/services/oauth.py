from abc import ABC, abstractmethod
from amichan.domain.dtos.user import OAuthUserDTO


class IOAuthService(ABC):
    """Interface for OAuth service."""

    @abstractmethod
    async def callback(self, code: str) -> OAuthUserDTO: ...

    @abstractmethod
    async def parse_jwt_token(self, token: str) -> OAuthUserDTO: ...

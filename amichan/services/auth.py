import re
from datetime import datetime, timedelta

from fastapi_mail import MessageSchema
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger

from amichan.domain.dtos.user import OAuthUserDTO, UserDTO

import jwt

from amichan.domain.repositories.auth import IAuthRepository
from amichan.domain.services.auth import IJWTService

logger = get_logger()

VALID_EMAIL_REGEX = r".+@edu\.hse\.ru$"


class EmailSchema(BaseModel):
    email: EmailStr


class JWTService(IJWTService):
    """Service to handle user auth logic via Yandex OAuth."""

    def __init__(self, secret_key: str, auth_repo: IAuthRepository) -> None:
        self._secret_key = secret_key
        self._auth_repo = auth_repo

    async def generate(self, email: str, role_id: int, exp: timedelta) -> str:
        expiration = datetime.utcnow() + exp
        payload = {"sub": email, "role": role_id, "exp": expiration}
        token = jwt.encode(payload, self._secret_key, algorithm="HS256")
        return token

    async def parse(self, token: str) -> UserDTO | None:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=["HS256"])
            return UserDTO(email=payload["sub"], role_id=payload["role"], token=token)
        except jwt.ExpiredSignatureError:
            logger.error("Token expired")
            return None
        except jwt.InvalidTokenError:
            logger.error("Invalid token")
            return None

    async def ban_user(
        self, session: AsyncSession, email: str, reason: str, duration: int
    ) -> None:
        if not re.match(VALID_EMAIL_REGEX, email):
            raise ValueError("Invalid email")
        await self._auth_repo.ban_user(session=session,email=email, reason=reason, duration=duration)

    async def login(
        self, session: AsyncSession, email: str, password: str
    ) -> UserDTO | None:
        role_id = await self._auth_repo.login(
            session=session, email=email, password=password
        )
        if role_id is None:
            return None

        return UserDTO(email=email, role_id=role_id, token="")

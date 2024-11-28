from datetime import datetime, timedelta

import jwt
from structlog import get_logger

from amichan.domain.dtos.jwt import AuthTokenDTO, JWTUserDTO
from amichan.domain.dtos.user import UserDTO
from amichan.domain.services.jwt import IJWTTokenService

logger = get_logger()


class JWTTokenService(IJWTTokenService):
    """Service to handle JWT tokens."""

    def __init__(
        self, secret_key: str, token_expiration_minutes: int, algorithm: str
    ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._token_expiration_minutes = token_expiration_minutes

    def generate_token(self, user: UserDTO) -> AuthTokenDTO:
        expire = datetime.now() + timedelta(minutes=self._token_expiration_minutes)
        payload = {"user_id": user.id, "role_id": user.role_id, "exp": expire}
        token = jwt.encode(payload, self._secret_key, algorithm=self._algorithm)
        return AuthTokenDTO(token=token)

    def get_user_info_from_token(self, auth_token: AuthTokenDTO) -> JWTUserDTO:
        try:
            payload = jwt.decode(
                auth_token.token, self._secret_key, algorithms=[self._algorithm]
            )
        except jwt.InvalidTokenError as err:
            logger.error("Invalid JWT token", token=auth_token.token, error=err)
            raise

        return JWTUserDTO(role=payload["role"])

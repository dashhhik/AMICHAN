from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger

from amichan.domain.dtos.user import OAuthUserDTO
from amichan.domain.services.auth import IUserAuthService

from amichan.domain.services.oauth import IOAuthService

logger = get_logger()


class UserAuthService(IUserAuthService):
    """Service to handle user auth logic via Yandex OAuth."""

    def __init__(self, oauth_service: IOAuthService):
        self._oauth_service = oauth_service

    async def sign_in_user(self, session: AsyncSession, oauth_token: str):
        """
        Handle OAuth-based sign-in via Yandex.

        :param session: AsyncSession for DB access (if needed).
        :param oauth_token: OAuth token provided by Yandex.
        :return: LoggedInUserDTO with user details.
        :raises UnauthorizedAccessException: If email is not valid for the domain.
        """
        try:
            # Получение информации о пользователе через OAuth сервис
            user_info: OAuthUserDTO = await self._oauth_service.get_user_info(
                oauth_token
            )
        except Exception as e:
            logger.error("Failed to retrieve user info via OAuth", error=str(e))
            raise

        # Проверка, что почта принадлежит домену @edu.hse.ru
        if not user_info.email.endswith("@edu.hse.ru"):
            logger.error("Unauthorized email domain", email=user_info.email)
            raise

        logger.info("User signed in successfully", email=user_info.email)
        return OAuthUserDTO(
            email=user_info.email,
            # token=oauth_token,  # Возвращаем сам OAuth токен
        )

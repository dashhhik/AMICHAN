import aiohttp

from amichan.api.routes.auth import TOKEN_URL
from amichan.domain.dtos.user import OAuthUserDTO
from amichan.domain.services.oauth import IOAuthService


class YandexOAuthService(IOAuthService):
    """Service to handle Yandex OAuth authentication."""

    USER_INFO_URL = "https://login.yandex.ru/info"

    async def callback(self, code: str) -> OAuthUserDTO:
        async with aiohttp.ClientSession() as session:
            data = {
                "grant_type": "authorization_code",
                "code": code,
            }
        async with session.post(TOKEN_URL, data=data) as response:
            token_data = await response.json()

        access_token = token_data.get("access_token")
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {access_token}"}
            async with session.get(
                    "https://login.yandex.ru/info", headers=headers
            ) as response:
                user_info = await response.json()

        return OAuthUserDTO(email=user_info.get("default_email"), token=access_token)

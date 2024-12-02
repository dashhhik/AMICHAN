import abc


class IUserAuthService(abc.ABC):
    """Interface for UserAuth service."""

    @abc.abstractmethod
    async def sign_in_user(self, oauth_token: str) -> None:
        """
        Sign in user using OAuth token.

        :param oauth_token: OAuth token provided by the client.
        """
        pass

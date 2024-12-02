from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from amichan.core.container import container
from amichan.services.board import BoardsService
from amichan.services.thread import ThreadService
from amichan.services.auth import UserAuthService
from amichan.services.oauth import YandexOAuthService

DBSession = Annotated[AsyncSession, Depends(container.session)]

IThreadService = Annotated[ThreadService, Depends(container.thread_service)]
IBoardsService = Annotated[BoardsService, Depends(container.board_service)]
IAuthService = Annotated[UserAuthService, Depends(container.user_auth_service)]
IOAuthService = Annotated[YandexOAuthService, Depends(container.oauth_service)]

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from amichan.core.security import HTTPTokenHeader
from amichan.core.container import container
from amichan.domain.dtos.user import UserDTO
from amichan.services.board import BoardsService
from amichan.services.thread import ThreadService
from amichan.services.auth import JWTService

DBSession = Annotated[AsyncSession, Depends(container.session)]

token_security = HTTPTokenHeader(
    name="Authorization",
    scheme_name="JWT Token",
    description="Token Format: `Token xxxxxx.yyyyyyy.zzzzzz`",
    raise_error=True,
)

JWTToken = Annotated[str, Depends(token_security)]

IThreadService = Annotated[ThreadService, Depends(container.thread_service)]
IBoardsService = Annotated[BoardsService, Depends(container.board_service)]
IJWTService = Annotated[JWTService, Depends(container.jwt_service)]


async def get_current_user(
    token: JWTToken,
    auth_token_service: IJWTService,
) -> UserDTO:
    jwt_user = await auth_token_service.parse(token=token)
    return jwt_user


CurrentUser = Annotated[UserDTO, Depends(get_current_user)]

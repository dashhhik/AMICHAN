from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from amichan.domain.dtos.board import BoardDTO
from amichan.domain.repositories.board import IBoardRepository
from amichan.domain.services.board import IBoardService


class BoardsService(IBoardService):
    """Service to handle boards logic."""

    def __init__(
        self,
        board_repo: IBoardRepository,
    ) -> None:
        self._board_repo = board_repo

    async def get_boards(self, session: AsyncSession) -> list[BoardDTO]:
        boards = await self._board_repo.get_all(
            session=session,
        )
        return [board for board in boards]

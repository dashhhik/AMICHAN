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

    async def create_new_board(
        self,
        session: AsyncSession,
        board_name: str,
        board_description: str,
    ) -> BoardDTO:
        board = await self._board_repo.create_board(
            session=session,
            board_name=board_name,
            board_description=board_description,
        )
        return board

    async def delete_board(self, session: AsyncSession, board_id: int) -> None:
        await self._board_repo.delete_board(
            session=session,
            board_id=board_id,
        )

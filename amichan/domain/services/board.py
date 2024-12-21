import abc
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from amichan.domain.dtos.board import BoardDTO


class IBoardService(abc.ABC):

    @abc.abstractmethod
    async def create_new_board(
        self,
        session: AsyncSession,
        board_name: str,
        board_description: str,
    ) -> BoardDTO: ...

    @abc.abstractmethod
    async def get_boards(self, session: AsyncSession) -> list[BoardDTO]: ...

    @abc.abstractmethod
    async def delete_board(self, session: AsyncSession, board_id: int) -> None: ...

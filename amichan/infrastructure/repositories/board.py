from typing import Any, List

from sqlalchemy import select

from amichan.domain.dtos.board import BoardDTO
from amichan.domain.mapper import IModelMapper
from amichan.domain.repositories.board import IBoardRepository
from amichan.infrastructure.models import Board


class BoardRepository(IBoardRepository):
    def __init__(self, board_mapper: IModelMapper[Board, BoardDTO]):
        self._board_mapper = board_mapper

    async def get_all(self, session: Any) -> list[BoardDTO]:
        query = select(Board)
        boards = await session.execute(query)
        return [self._board_mapper.to_dto(board) for board in boards.scalars()]

    async def create_board(
        self,
        session: Any,
        board_name: str,
        board_description: str,
    ) -> BoardDTO:
        board = Board(name=board_name, description=board_description)
        session.add(board)
        await session.commit()
        return self._board_mapper.to_dto(board)

    async def delete_board(self, session: Any, board_id: int) -> None:
        query = select(Board).filter(Board.id == board_id)
        board = await session.execute(query)
        session.delete(board.scalar())
        await session.commit()

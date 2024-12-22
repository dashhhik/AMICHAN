from datetime import datetime
from typing import Any, List

from sqlalchemy import select, insert
from sqlalchemy.exc import SQLAlchemyError

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
        if not board_name or not board_description:
            raise ValueError("Board name and description must be provided.")

        # Ensure the column names match your Board table schema
        query = (
            insert(Board)
            .values(
                name=board_name,
                description=board_description,
                created_at=datetime.utcnow(),  # Use UTC for consistency
                updated_at=datetime.utcnow(),
            )
            .returning(Board)  # Ensure this works in your setup
        )

        try:
            result = await session.execute(query)
            board = result.scalar()
            if not board:
                raise ValueError("Failed to insert board into the database.")

        # Return the mapped DTO
            return self._board_mapper.to_dto(board)
        except SQLAlchemyError as e:
            await session.rollback()  # Rollback on failure
            raise RuntimeError(f"Database error occurred: {e}") from e

    async def delete_board(self, session: Any, board_id: int) -> None:
        query = select(Board).where(Board.id == board_id)
        board_result = await session.execute(query)
        board = board_result.scalar()
        if board is None:
            raise ValueError(f"Thread with id {board_id} not found")  # Handle the case where the board does not exist

        await session.delete(board)
        await session.commit()


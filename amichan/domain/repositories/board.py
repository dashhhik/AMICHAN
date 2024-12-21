import abc
from typing import Any, List

from amichan.domain.dtos.board import BoardDTO


class IBoardRepository(abc.ABC):
    """Board repository interface."""

    @abc.abstractmethod
    async def get_all(self, session: Any) -> list[BoardDTO]: ...

    @abc.abstractmethod
    async def create_board(
        self,
        session: Any,
        board_name: str,
        board_description: str,
    ) -> BoardDTO: ...

    @abc.abstractmethod
    async def delete_board(self, session: Any, board_id: int) -> None: ...

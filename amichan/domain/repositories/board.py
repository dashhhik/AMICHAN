import abc
from typing import List

from amichan.domain.dtos.board import (
    BoardDTO,
    BoardCreateDTO,
)


class IBoardRepository(abc.ABC):
    """Board repository interface."""

    @abc.abstractmethod
    def create(self, board: BoardCreateDTO) -> BoardDTO: ...

    @abc.abstractmethod
    def get(self, board_id: int) -> BoardDTO: ...

    @abc.abstractmethod
    def get_all(self) -> List[BoardDTO]: ...

    @abc.abstractmethod
    def delete(self, board_id: int) -> None: ...

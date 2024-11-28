import abc
from typing import Any, List

from amichan.domain.dtos.board import BoardDTO


class IBoardRepository(abc.ABC):
    """Board repository interface."""

    @abc.abstractmethod
    async def get_all(self, session: Any) -> list[BoardDTO]: ...

import abc
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from amichan.domain.dtos.board import BoardDTO


class IBoardService(abc.ABC):

    @abc.abstractmethod
    async def get_boards(self, session: AsyncSession) -> list[BoardDTO]: ...

import abc
from typing import Any, List

from amichan.domain.dtos.thread import CreateThreadDTO, ThreadRecordDTO


class IThreadRepository(abc.ABC):
    """Thread repository interface."""

    @abc.abstractmethod
    async def create(
        self, session: Any, create_item: CreateThreadDTO
    ) -> ThreadRecordDTO: ...

    @abc.abstractmethod
    async def get(self, session: Any, thread_id: int) -> ThreadRecordDTO: ...

    @abc.abstractmethod
    async def get_all(self, session: Any, board_id: int) -> list[ThreadRecordDTO]: ...

import abc
from typing import Any

from amichan.domain.dtos.thread import CreateThreadDTO, ThreadRecordDTO, ThreadsFeedDTO


class IThreadService(abc.ABC):

    @abc.abstractmethod
    async def create_new_thread(
        self,
        session: Any,
        author_nickname: str | None,
        thread_to_create: CreateThreadDTO,
    ) -> ThreadRecordDTO: ...

    @abc.abstractmethod
    async def get_thread_by_id(
        self, session: Any, thread_id: int
    ) -> ThreadRecordDTO: ...

    @abc.abstractmethod
    async def get_threads(self, session: Any, board_id: int) -> ThreadsFeedDTO: ...
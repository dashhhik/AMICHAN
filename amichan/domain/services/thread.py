import abc
from typing import Any

from amichan.domain.dtos.thread import CreateThreadDTO, ThreadRecordDTO, ThreadsFeedDTO, ThreadPostsDTO


class IThreadService(abc.ABC):

    @abc.abstractmethod
    async def create_new_thread(
        self,
        session: Any,
        board_id: int,
        thread_to_create: CreateThreadDTO,
    ) -> ThreadRecordDTO: ...

    @abc.abstractmethod
    async def get_thread_by_id(
        self, session: Any, thread_id: int
    ) -> ThreadPostsDTO: ...

    @abc.abstractmethod
    async def get_threads(self, session: Any, board_id: int) -> ThreadsFeedDTO: ...

    @abc.abstractmethod
    async def delete_thread(self, session: Any, thread_id: int) -> None: ...

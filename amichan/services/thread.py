from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from amichan.core.exceptions import ThreadNotFoundException
from amichan.domain.dtos.thread import CreateThreadDTO, ThreadRecordDTO, ThreadsFeedDTO
from amichan.domain.repositories.thread import IThreadRepository
from amichan.domain.services.thread import IThreadService


class ThreadService(IThreadService):
    """Service to handle threads logic."""

    def __init__(self, thread_repo: IThreadRepository) -> None:
        self._thread_repo = thread_repo

    async def create_new_thread(
        self,
        session: Any,
        author_nickname: str | None,
        thread_to_create: CreateThreadDTO,
    ) -> ThreadRecordDTO:
        return await self._thread_repo.create(
            session=session,
            create_item=thread_to_create,
        )

    async def get_thread_by_id(self, session: Any, thread_id: int) -> ThreadRecordDTO:
        thread = await self._thread_repo.get(session=session, thread_id=thread_id)
        if thread is None:
            raise ThreadNotFoundException(f"Thread with ID {thread_id} not found")
        return thread

    async def get_threads(self, session: AsyncSession, board_id: int) -> ThreadsFeedDTO:
        threads = await self._thread_repo.get_all(session=session, board_id=board_id)
        return ThreadsFeedDTO(threads=threads, threads_count=len(threads))

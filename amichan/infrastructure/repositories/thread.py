from datetime import datetime
from typing import Any, List

from sqlalchemy import insert, select

from amichan.domain.dtos.thread import CreateThreadDTO, ThreadRecordDTO
from amichan.domain.mapper import IModelMapper
from amichan.domain.repositories.thread import IThreadRepository
from amichan.infrastructure.models import Thread


class ThreadRepository(IThreadRepository):
    def __init__(self, thread_mapper: IModelMapper[Thread, ThreadRecordDTO]):
        self._thread_mapper = thread_mapper

    async def create(
        self, session: Any, create_item: CreateThreadDTO
    ) -> ThreadRecordDTO:
        query = (
            insert(Thread)
            .values(
                board_id=create_item.board_id,
                title=create_item.title,
                content=create_item.content,
                created_at=datetime.now(),
                nickname=create_item.nickname,
                tag=create_item.tag,
            )
            .returning(Thread)
        )
        result = await session.execute(query)
        thread = result.scalar()
        if thread is None:
            raise ValueError("Failed to insert thread")  # Add error handling
        return self._thread_mapper.to_dto(thread)

    async def get(self, session: Any, thread_id: int) -> ThreadRecordDTO:
        query = select(Thread)

        thread = await session.execute(query)

        th = thread.scalars().first()

        # Log the result of the query
        print(f"Thread query result for id {thread_id}: {th}")

        return self._thread_mapper.to_dto(thread)

    async def get_all(self, session: Any, board_id: int) -> list[ThreadRecordDTO]:
        print(f"Getting all threads for board {board_id}")
        query = select(Thread)
        result = await session.execute(query)
        return [self._thread_mapper.to_dto(thread) for thread in result]

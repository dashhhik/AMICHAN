from datetime import datetime
from typing import Any, List

from sqlalchemy import insert, select

from amichan.domain.dtos.thread import CreateThreadDTO, ThreadRecordDTO, ThreadPostsDTO
from amichan.domain.mapper import IModelMapper
from amichan.domain.repositories.thread import IThreadRepository
from amichan.infrastructure.models import Thread, Post


class ThreadRepository(IThreadRepository):
    def __init__(
        self,
        thread_mapper: IModelMapper[Thread, ThreadRecordDTO],
        post_mapper: IModelMapper[Post, Any],
    ):
        self._thread_mapper = thread_mapper
        self._post_mapper = post_mapper

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
            )
            .returning(Thread)
        )
        result = await session.execute(query)
        thread = result.scalar()
        if thread is None:
            raise ValueError("Failed to insert thread")  # Add error handling
        return self._thread_mapper.to_dto(thread)

    async def get(self, session: Any, thread_id: int) -> ThreadPostsDTO:
        thread_query = select(Thread).where(Thread.id == thread_id)
        thread_result = await session.execute(thread_query)
        thread = thread_result.scalar()
        if thread is None:
            raise ValueError(f"Thread with id {thread_id} not found")

        posts_query = select(Post).where(Post.thread_id == thread_id)
        posts_result = await session.execute(posts_query)
        posts = posts_result.scalars().all()

        thread_dto = self._thread_mapper.to_dto(thread)
        posts_dto = [self._post_mapper.to_dto(post) for post in posts]

        return ThreadPostsDTO(thread=thread_dto, posts=posts_dto)

    async def get_all(self, session: Any, board_id: int) -> List[ThreadRecordDTO]:
        query = select(Thread).where(Thread.board_id == board_id)
        result = await session.execute(query)
        threads = result.scalars().all()
        return [self._thread_mapper.to_dto(thread) for thread in threads]

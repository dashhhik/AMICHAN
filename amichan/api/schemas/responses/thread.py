import datetime
from typing import List

from pydantic import BaseModel

from amichan.api.schemas.responses.post import PostResponse
from amichan.domain.dtos.thread import ThreadRecordDTO, ThreadsFeedDTO, ThreadPostsDTO


class ThreadData(BaseModel):
    id: int
    title: str
    content: str
    created_at: str
    replies_count: int
    nickname: str | None = None
    is_deleted: bool = False


class ThreadResponse(BaseModel):
    thread: ThreadData

    @classmethod
    def from_dto(cls, dto: ThreadRecordDTO) -> "ThreadResponse":
        thread = ThreadData(
            id=dto.id,
            title=dto.title,
            content=dto.content,
            created_at=dto.created_at.isoformat(),
            replies_count=dto.replies_count,
            nickname=dto.nickname,
            is_deleted=dto.is_deleted,
        )
        return ThreadResponse(thread=thread)


class ThreadFeedResponse(BaseModel):
    threads: list[ThreadData]
    threads_count: int

    @classmethod
    def from_dto(cls, dto: ThreadsFeedDTO) -> "ThreadFeedResponse":
        threads = [
            ThreadResponse.from_dto(dto=thread_dto).thread for thread_dto in dto.threads
        ]
        threads_count = len(threads)
        return ThreadFeedResponse(threads=threads, threads_count=threads_count)


class ThreadPostsResponse(BaseModel):
    thread: ThreadResponse
    posts: List[PostResponse]

    @classmethod
    def from_dto(cls, dto: ThreadPostsDTO) -> "ThreadPostsResponse":
        thread_data = ThreadResponse.from_dto(dto.thread)
        posts_data = [PostResponse.from_dto(post) for post in dto.posts]
        return cls(thread=thread_data, posts=posts_data)

import datetime

from pydantic import BaseModel

from amichan.domain.dtos.thread import ThreadRecordDTO, ThreadsFeedDTO


class ThreadData(BaseModel):
    title: str
    content: str
    created_at: datetime.datetime
    replies_count: int
    nickname: str | None = None
    is_deleted: bool = False


class ThreadResponse(BaseModel):
    thread: ThreadData

    @classmethod
    def from_dto(cls, dto: ThreadRecordDTO) -> "ThreadResponse":
        thread = ThreadData(
            title=dto.title,
            content=dto.content,
            created_at=dto.created_at,
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

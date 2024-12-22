import datetime
from dataclasses import dataclass

from amichan.domain.dtos.post import PostDTO


@dataclass(frozen=True)
class ThreadRecordDTO:
    id: int
    board_id: int
    title: str
    content: str
    created_at: str
    replies_count: int
    nickname: str
    is_deleted: bool


@dataclass(frozen=True)
class ThreadPostsDTO:
    thread: ThreadRecordDTO
    posts: list[PostDTO]


@dataclass(frozen=True)
class ThreadsFeedDTO:
    threads: list[ThreadRecordDTO]
    threads_count: int


@dataclass(frozen=True)
class CreateThreadDTO:
    title: str
    content: str
    nickname: str | None = None

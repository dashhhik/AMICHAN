import datetime
from dataclasses import dataclass

from amichan.domain.dtos.post import PostDTO


@dataclass(frozen=True)
class ThreadDTO:
    id: int
    board_id: int
    title: str
    content: str
    created_at: datetime.datetime
    replies_count: int
    nickname: str
    is_deleted: bool


@dataclass(frozen=True)
class ThreadRecordDTO:
    id: int
    board_id: int
    title: str
    content: str
    created_at: datetime.datetime
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
    board_id: int
    title: str
    content: str
    created_at: str
    nickname: str | None = None

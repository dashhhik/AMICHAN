import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PostDTO:
    id: int
    thread_id: int
    content: str
    created_at: datetime.datetime
    nickname: str
    is_deleted: bool
    replies_count: int
    parent_id: int | None = None


@dataclass(frozen=True)
class PostCreateDTO:
    parent_id: int
    content: str
    nickname: str | None = None

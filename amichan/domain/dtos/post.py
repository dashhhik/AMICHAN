import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class PostDTO:
    id: int
    thread_id: int
    parent_id: int
    content: str
    created_at: datetime.datetime
    nickname: str
    is_moderator: bool
    is_deleted: bool
    replies_count: int


@dataclass(frozen=True)
class PostCreateDTO:
    thread_id: int
    parent_id: int
    content: str
    nickname: str
    is_moderator: bool

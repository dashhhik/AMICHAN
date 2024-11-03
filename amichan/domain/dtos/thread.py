import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class ThreadDTO:
    id: int
    board_id: int
    tag_id: int
    title: str
    content: str
    created_at: datetime.datetime
    replies_count: int
    nickname: str
    is_moderator: bool
    is_deleted: bool


@dataclass(frozen=True)
class ThreadCreateDTO:
    board_id: int
    tag_id: int
    title: str
    content: str
    nickname: str
    is_moderator: bool

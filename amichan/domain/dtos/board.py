import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class BoardDTO:
    id: int
    name: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    threads_count: int


@dataclass(frozen=True)
class BoardCreateDTO:
    name: str
    description: str

import abc
from typing import List

from amichan.domain.dtos.thread import (
    ThreadDTO,
)


class IThreadTag(abc.ABC):
    """Thread Tag repository interface."""

    @abc.abstractmethod
    def create(self, thread_id: int, tag: str) -> None: ...

    @abc.abstractmethod
    def get_all_by_tag(self, tag_id: int) -> List[ThreadDTO]: ...

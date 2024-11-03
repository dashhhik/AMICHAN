import abc
from typing import List

from amichan.domain.dtos.thread import (
    ThreadDTO,
    ThreadCreateDTO,
)


class IThreadRepository(abc.ABC):
    """Thread repository interface."""

    @abc.abstractmethod
    def create(self, thread: ThreadCreateDTO) -> ThreadDTO: ...

    @abc.abstractmethod
    def get(self, thread_id: int) -> ThreadDTO: ...

    @abc.abstractmethod
    def get_all(self, board_id: int) -> List[ThreadDTO]: ...

    @abc.abstractmethod
    def delete(self, thread_id: int) -> None: ...

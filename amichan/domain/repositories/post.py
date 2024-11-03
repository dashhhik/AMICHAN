import abc
from typing import List

from amichan.domain.dtos.post import PostDTO, PostCreateDTO


class IPostRepository(abc.ABC):
    """Board repository interface."""

    @abc.abstractmethod
    def create(self, post: PostCreateDTO) -> PostDTO: ...

    @abc.abstractmethod
    def get(self, post_id: int) -> PostDTO: ...

    @abc.abstractmethod
    def get_all(self, thread_id: int) -> List[PostDTO]: ...

    @abc.abstractmethod
    def delete(self, post_id: int) -> None: ...

import abc
from typing import List, Any

from amichan.domain.dtos.post import PostDTO, PostCreateDTO


class IPostRepository(abc.ABC):
    """Post repository interface."""

    @abc.abstractmethod
    async def create(self, session: Any, create_item: PostCreateDTO) -> PostDTO: ...

    @abc.abstractmethod
    async def get_all_by_thread(self,session: Any, thread_id: int) -> List[PostDTO]: ...

    @abc.abstractmethod
    async def get_by_id(self,session: Any, post_id: int) -> PostDTO: ...


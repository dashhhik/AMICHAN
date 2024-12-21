import abc
from typing import Any, List

from amichan.domain.dtos.post import PostDTO, PostCreateDTO


class IPostService(abc.ABC):

    @abc.abstractmethod
    async def create_post(
            self,
            session: Any,
            post_to_create: PostCreateDTO,
    ) -> PostDTO:
        ...

    @abc.abstractmethod
    async def get_post_by_id(self, session: Any, post_id: int) -> PostDTO:        ...

    @abc.abstractmethod
    async def get_posts_by_thread(self, session: Any, thread_id: int) -> List[PostDTO]: ...

    @abc.abstractmethod
    async def delete_post(self, session: Any, post_id: int) -> None: ...

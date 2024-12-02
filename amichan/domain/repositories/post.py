import abc
from typing import List, Any

from amichan.domain.dtos.post import PostDTO, PostCreateDTO


class IPostRepository(abc.ABC):
    """Post repository interface."""

    @abc.abstractmethod
    async def create(self, session: Any, create_item: PostCreateDTO) -> PostDTO: ...

    @abc.abstractmethod
    async def get_all(self, thread_id: int) -> List[PostDTO]:
        """
        Abstract method to retrieve all posts in a thread.

        Args:
            thread_id: The ID of the thread to retrieve posts from.

        Returns:
            A list of `PostDTO` objects representing all posts in the thread.
        """
        pass

    @abc.abstractmethod
    async def delete(self, post_id: int) -> None:
        """
        Abstract method to delete a post by its ID.

        Args:
            post_id: The ID of the post to delete.

        Returns:
            None
        """
        pass

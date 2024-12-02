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
        """
        Create a new post.

        Args:
            session: The database session.
            post_to_create: The DTO containing the details of the post to create.

        Returns:
            The created PostDTO.
        """
        ...

    @abc.abstractmethod
    async def get_post_by_id(self, session: Any, post_id: int) -> PostDTO:
        """
        Retrieve a single post by its ID.

        Args:
            session: The database session.
            post_id: The ID of the post to retrieve.

        Returns:
            The PostDTO corresponding to the post.
        """
        ...

    @abc.abstractmethod
    async def get_posts_by_thread(self, session: Any, thread_id: int) -> List[PostDTO]:
        """
        Retrieve all posts for a specific thread.

        Args:
            session: The database session.
            thread_id: The ID of the thread.

        Returns:
            A list of PostDTO objects.
        """
        ...

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from amichan.domain.dtos.post import PostDTO, PostCreateDTO
from amichan.domain.repositories.post import IPostRepository
from amichan.domain.services.post import IPostService


class PostService(IPostService):
    """Service to handle posts logic."""

    def __init__(
            self,
            post_repo: IPostRepository,
    ) -> None:
        self._post_repo = post_repo

    async def get_posts_by_thread(
            self, session: AsyncSession, thread_id: int
    ) -> list[PostDTO]:
        """
        Retrieve all posts in a thread.

        Args:
            session: The database session.
            thread_id: The ID of the thread to retrieve posts for.

        Returns:
            A list of PostDTO objects.
        """
        posts = await self._post_repo.get_all_by_thread(
            session=session,
            thread_id=thread_id,
        )
        return [post for post in posts]

    async def create_post(
            self, session: AsyncSession, thread_id: int, post_create_dto: PostCreateDTO
    ) -> PostDTO:
        """
        Create a new post.

        Args:
            session: The database session.
            post_create_dto: The PostCreateDTO object containing post details.

        Returns:
            The created PostDTO object.
        """
        post = await self._post_repo.create(
            session=session,
            create_item=post_create_dto,
            thread_id=thread_id,
        )
        return post

    async def get_post_by_id(self, session: AsyncSession, post_id: int) -> PostDTO:
        """
        Retrieve a single post by its ID.

        Args:
            session: The database session.
            post_id: The ID of the post to retrieve.

        Returns:
            A PostDTO object representing the post.
        """
        post = await self._post_repo.get_by_id(
            session=session,
            post_id=post_id,
        )
        return post

    async def delete_post(self, session: AsyncSession, post_id: int) -> None:
        """
        Delete a post by its ID.

        Args:
            session: The database session.
            post_id: The ID of the post to delete.
        """
        await self._post_repo.delete(
            session=session,
            post_id=post_id,
        )

from datetime import datetime
from typing import Any, List

from sqlalchemy import insert, select

from amichan.domain.dtos.post import PostCreateDTO, PostDTO
from amichan.domain.mapper import IModelMapper
from amichan.domain.repositories.post import IPostRepository
from amichan.infrastructure.models import Post


class PostRepository(IPostRepository):
    def __init__(self, post_mapper: IModelMapper[Post, PostDTO]):
        self._post_mapper = post_mapper

    async def create(self, session: Any, create_item: PostCreateDTO) -> PostDTO:
        """
        Create a new post and return its DTO representation.
        """
        query = (
            insert(Post)
            .values(
                thread_id=create_item.thread_id,
                parent_id=create_item.parent_id,
                content=create_item.content,
                created_at=datetime.now(),
                nickname=create_item.nickname,
                is_deleted=False,
                replies_count=0,
            )
            .returning(Post)
        )
        result = await session.execute(query)
        post = result.scalar()
        if post is None:
            raise ValueError("Failed to insert post")  # Add error handling
        return self._post_mapper.to_dto(post)

    async def get_by_id(self, session: Any, post_id: int) -> PostDTO:
        """
        Retrieve a single post by its ID.
        """
        query = select(Post).where(Post.id == post_id)
        result = await session.execute(query)
        post = result.scalar()
        if post is None:
            raise ValueError(f"Post with id {post_id} not found")
        return self._post_mapper.to_dto(post)

    async def get_all_by_thread(self, session: Any, thread_id: int) -> List[PostDTO]:
        """
        Retrieve all posts belonging to a specific thread.
        """
        query = select(Post).where(Post.thread_id == thread_id)
        result = await session.execute(query)
        posts = result.scalars().all()
        return [self._post_mapper.to_dto(post) for post in posts]

    async def delete(self, session: Any, post_id: int) -> None:
        """
        Delete a post by its ID.
        """
        query = select(Post).where(Post.id == post_id)
        post = await session.execute(query)
        session.delete(post.scalar())
        await session.commit()

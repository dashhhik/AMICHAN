import datetime

from amichan.domain.dtos.post import PostDTO, PostCreateDTO
from amichan.domain.mapper import IModelMapper
from amichan.infrastructure.models import Post


class PostModelMapper(IModelMapper[Post, PostDTO]):

    @staticmethod
    def to_dto(model: Post) -> PostDTO:
        """
        Converts a Post ORM model to a PostDTO.
        """
        if model is None:
            raise ValueError("Cannot convert None to PostDTO")

        return PostDTO(
            id=model.id,
            thread_id=model.thread_id,
            parent_id=model.parent_id,
            content=model.content,
            created_at=model.created_at,
            nickname=model.nickname,
            is_deleted=model.is_deleted,
            replies_count=model.replies_count,
        )

    @staticmethod
    def from_dto(dto: PostDTO) -> Post:
        """
        Converts a PostDTO back to a Post ORM model.
        """
        if dto is None:
            raise ValueError("Cannot convert None to Post model")

        model = Post(
            id=dto.id,
            thread_id=dto.thread_id,
            parent_id=dto.parent_id,
            content=dto.content,
            created_at=dto.created_at,
            nickname=dto.nickname,
            is_deleted=dto.is_deleted,
            replies_count=dto.replies_count,
        )
        return model

    @staticmethod
    def from_create_dto(dto: PostCreateDTO) -> Post:
        """
        Converts a PostCreateDTO to a Post ORM model.
        """
        if dto is None:
            raise ValueError("Cannot convert None to Post model")

        model = Post(
            thread_id=dto.thread_id,
            parent_id=dto.parent_id,
            content=dto.content,
            nickname=dto.nickname,
            created_at=datetime.datetime.now(),  # Assign current time
            is_deleted=False,  # Default to not deleted
            replies_count=0,  # Default replies count
        )
        return model

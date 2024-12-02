from typing import Optional

from pydantic import BaseModel

from amichan.domain.dtos.post import PostDTO


class PostResponse(BaseModel):
    id: int
    content: str
    created_at: str
    nickname: str | None = None  # Опциональное поле
    parent_id: int | None = None  # Опциональное поле

    @classmethod
    def from_dto(cls, dto: PostDTO):
        return cls(
            id=dto.id,
            content=dto.content,
            created_at=dto.created_at.isoformat(),
            nickname=dto.nickname,
            parent_id=dto.parent_id,
        )

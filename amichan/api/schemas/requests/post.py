from pydantic import BaseModel

from amichan.domain.dtos.post import PostCreateDTO


class PostCreateRequest(BaseModel):
    parent_id: int
    nickname: str | None = None
    content: str

    def to_dto(self) -> PostCreateDTO:
        return PostCreateDTO(
            parent_id=self.parent_id,
            nickname=self.nickname,
            content=self.content,
        )



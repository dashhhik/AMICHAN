from typing import Optional

from pydantic import BaseModel


class PostResponse(BaseModel):
    id: int
    content: str
    created_at: str
    nickname: str | None = None  # Опциональное поле
    parent: Optional["PostResponse"] = None  # Рекурсивное определение

    class Config:
        orm_mode = True  # Для работы с ORM-объектами


PostResponse.model_rebuild()

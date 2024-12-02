from pydantic import BaseModel, Field

from amichan.domain.dtos.thread import CreateThreadDTO

DEFAULT_THREAD_LIMIT = 20
DEFAULT_THREAD_OFFSET = 0


class ThreadFilters(BaseModel):
    limit: int = Field(DEFAULT_THREAD_LIMIT, ge=1)
    offset: int = Field(DEFAULT_THREAD_OFFSET, ge=0)


class CreateThreadData(BaseModel):
    board_id: int
    title: str
    content: str
    created_at: str
    nickname: str | None = None


class CreateThreadRequest(BaseModel):
    thread: CreateThreadData

    def to_dto(self) -> CreateThreadDTO:
        return CreateThreadDTO(
            board_id=self.thread.board_id,
            title=self.thread.title,
            content=self.thread.content,
            created_at=self.thread.created_at,
            nickname=self.thread.nickname,
        )

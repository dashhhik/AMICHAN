from pydantic import BaseModel, Field

from amichan.domain.dtos.thread import CreateThreadDTO

DEFAULT_THREAD_LIMIT = 20
DEFAULT_THREAD_OFFSET = 0


class ThreadFilters(BaseModel):
    limit: int = Field(DEFAULT_THREAD_LIMIT, ge=1)
    offset: int = Field(DEFAULT_THREAD_OFFSET, ge=0)


class CreateThreadData(BaseModel):
    title: str
    content: str
    nickname: str | None = None


class CreateThreadRequest(BaseModel):
    thread: CreateThreadData

    def to_dto(self) -> CreateThreadDTO:
        return CreateThreadDTO(
            title=self.thread.title,
            content=self.thread.content,
            nickname=self.thread.nickname,
        )

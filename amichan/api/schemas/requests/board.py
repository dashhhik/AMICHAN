from pydantic import BaseModel

from amichan.domain.dtos.board import CreateBoardDTO


class BoardCreateRequest(BaseModel):
    name: str
    description: str

    def to_dto(self) -> CreateBoardDTO:
        return CreateBoardDTO(
            name=self.name,
            description=self.description,
        )

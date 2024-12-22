import datetime

from pydantic import BaseModel

from amichan.domain.dtos.board import BoardDTO


class BoardsData(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: str
    updated_at: str
    threads_count: int


class BoardResponse(BaseModel):
    board: BoardsData

    @classmethod
    def from_dto(cls, dto: BoardDTO) -> "BoardResponse":
        board = BoardsData(
            id=dto.id,
            name=dto.name,
            description=dto.description,
            created_at=dto.created_at.isoformat(),
            updated_at=dto.updated_at.isoformat(),
            threads_count=dto.threads_count,
        )
        return BoardResponse(board=board)


class BoardsResponse(BaseModel):
    boards: list[BoardsData]

    @classmethod
    def from_dto(cls, dto: list[BoardDTO]) -> "BoardsResponse":
        boards = [BoardResponse.from_dto(dto=board_dto).board for board_dto in dto]
        return BoardsResponse(boards=boards)

from amichan.domain.dtos.board import BoardDTO
from amichan.domain.mapper import IModelMapper
from amichan.infrastructure.models import Board


class BoardModelMapper(IModelMapper[Board, BoardDTO]):
    @staticmethod
    def to_dto(model: Board) -> BoardDTO:
        """
        Converts a Thread ORM model to a ThreadRecordDTO.
        """
        dto = BoardDTO(
            id=model.id,
            name=model.name,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
            threads_count=model.threads_count,
        )
        return dto

    @staticmethod
    def from_dto(dto: BoardDTO) -> Board:
        """
        Converts a ThreadRecordDTO back to a Thread ORM model.
        """
        model = Board(
            name=dto.name,
            description=dto.description,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            threads_count=dto.threads_count,
        )
        if hasattr(dto, "id"):
            model.id = dto.id
        return model

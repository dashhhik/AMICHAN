from amichan.domain.dtos.thread import ThreadRecordDTO
from amichan.domain.mapper import IModelMapper
from amichan.infrastructure.models import Thread


class ThreadModelMapper(IModelMapper[Thread, ThreadRecordDTO]):

    @staticmethod
    def to_dto(model: Thread) -> ThreadRecordDTO:
        """
        Converts a Thread ORM model to a ThreadRecordDTO.
        """
        if model is None:
            raise ValueError("Cannot convert None to ThreadRecordDTO")

        return ThreadRecordDTO(
            id=model.id,
            board_id=model.board_id,
            title=model.title,
            content=model.content,
            created_at=model.created_at,
            replies_count=model.replies_count,
            nickname=model.nickname,
            is_deleted=model.is_deleted,
        )

    @staticmethod
    def from_dto(dto: ThreadRecordDTO) -> Thread:
        """
        Converts a ThreadRecordDTO back to a Thread ORM model.
        """
        if dto is None:
            raise ValueError("Cannot convert None to Thread model")

        model = Thread(
            board_id=dto.board_id,
            title=dto.title,
            content=dto.content,
            created_at=dto.created_at,
            replies_count=dto.replies_count,
            nickname=dto.nickname,
            is_deleted=dto.is_deleted,
        )
        if hasattr(dto, "id"):
            model.id = dto.id
        return model

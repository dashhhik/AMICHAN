from amichan.domain.dtos.user import AdminDTO, BanListDTO

from amichan.domain.mapper import IModelMapper
from amichan.infrastructure.models import Admins, BanList


class AdminModelMapper(IModelMapper[Admins, AdminDTO]):
    @staticmethod
    def to_dto(model: Admins) -> AdminDTO:
        """
        Converts an Admin ORM model to an AdminDTO.
        """
        dto = AdminDTO(
            id=model.id,
            email=model.email,
            password_hash=model.password_hash,
            role_id=model.role_id,
        )
        return dto

    @staticmethod
    def from_dto(dto: AdminDTO) -> Admins:
        """
        Converts an AdminDTO back to an Admin ORM model.
        """
        model = Admins(
            email=dto.email,
            password_hash=dto.password_hash,
            role_id=dto.role_id,
        )
        if hasattr(dto, "id"):
            model.id = dto.id
        return model


class BanListModelMapper(IModelMapper[BanList, BanListDTO]):
    @staticmethod
    def to_dto(model: BanList) -> BanListDTO:
        """
        Converts a BanList ORM model to a BanListDTO.
        """
        dto = BanListDTO(
            id=model.id,
            email=model.email,
            reason=model.reason,
            banned_at=model.banned_at,
            expires_at=model.expires_at,
        )
        return dto

    @staticmethod
    def from_dto(dto: BanListDTO) -> BanList:
        """
        Converts a BanListDTO back to a BanList ORM model.
        """
        model = BanList(
            email=dto.email,
            reason=dto.reason,
            banned_at=dto.banned_at,
            expires_at=dto.expires_at,
        )
        if hasattr(dto, "id"):
            model.id = dto.id
        return model

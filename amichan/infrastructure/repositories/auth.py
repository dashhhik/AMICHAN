from typing import Any

from sqlalchemy.testing.pickleable import User
from amichan.domain.dtos.user import AdminDTO
from amichan.domain.dtos.user import UserDTO, BanListDTO
from amichan.domain.mapper import IModelMapper
from amichan.domain.repositories.auth import IAuthRepository
from amichan.infrastructure.models import Admins, BanList
from sqlalchemy import select


class AuthRepository(IAuthRepository):
    def __init__(
            self,
            admin_mapper: IModelMapper[Admins, AdminDTO],
            ban_list_mapper: IModelMapper[BanList, BanListDTO],
    ):
        self._admin_mapper = admin_mapper
        self._ban_list_mapper = ban_list_mapper

    async def ban_user(
            self, session: Any, email: str, reason: str, duration: int
    ) -> None:
        from datetime import datetime, timedelta

        ban_entry = BanList(
            email=email,
            reason=reason,
            banned_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=duration),
        )
        session.add(ban_entry)
        await session.commit()

    async def login(self, session: Any, email:str, password:str) -> int:
        password = hash_password(password)
        query = select(Admins).filter(Admins.email == email, Admins.password_hash == password)
        result = await session.execute(query)
        user = result.scalar()
        if user:
            return user.id
        return 0

    # async def get_user(self, session: Any, email: str) -> UserDTO:
    #     query = select(User).filter(User.email == email)
    #     result = await session.execute(query)
    #     user = result.scalar()
    #     if user:
    #         return self._user_mapper.to_dto(user)
    #     raise ValueError("User not found")
    #
    # async def get_admin(self, session: Any, admin_id: int) -> AdminDTO:
    #     query = select(Admin).filter(Admin.id == admin_id)
    #     result = await session.execute(query)
    #     admin = result.scalar()
    #     if admin:
    #         return self._admin_mapper.to_dto(admin)
    #     raise ValueError("Admin not found")


def hash_password(password:str) -> str:
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

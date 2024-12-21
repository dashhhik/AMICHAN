from pydantic import BaseModel, EmailStr

from amichan.domain.dtos.user import BanUserDTO


class BanUserRequest(BaseModel):
    email: EmailStr
    reason: str
    duration: int

    def to_dto(self) -> BanUserDTO:
        return BanUserDTO(
            email=self.email,
            reason=self.reason,
            duration=self.duration,
        )

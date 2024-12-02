from dataclasses import dataclass


@dataclass(frozen=True)
class UserDTO:
    id: int
    role_id: int


@dataclass(frozen=True)
class OAuthUserDTO:
    email: str
    token: str

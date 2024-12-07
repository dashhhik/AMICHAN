from dataclasses import dataclass


@dataclass(frozen=True)
class UserDTO:
    email: str
    role_id: int
    token: str


@dataclass(frozen=True)
class OAuthUserDTO:
    email: str
    token: str

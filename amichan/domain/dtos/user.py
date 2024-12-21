import datetime
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


@dataclass(frozen=True)
class BanUserDTO:
    email: str
    reason: str
    duration: int


@dataclass(frozen=True)
class AdminDTO:
    id: int
    email: str
    password_hash: str
    role_id: int


@dataclass(frozen=True)
class BanListDTO:
    id: int
    email: str
    reason: str
    banned_at: datetime.datetime
    expires_at: datetime.datetime

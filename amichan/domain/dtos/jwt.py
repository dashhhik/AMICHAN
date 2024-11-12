from dataclasses import dataclass


@dataclass(frozen=True)
class AuthTokenDTO:
    token: str


@dataclass(frozen=True)
class JWTUserDTO:
    role: str

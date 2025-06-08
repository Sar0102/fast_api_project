from typing import Annotated

from pydantic import BaseModel, PrivateAttr


class UserDTO(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool
    permissions: list[str] | None = (None,)

    password: Annotated[str | None, PrivateAttr(default=None)] = None


class UserCreateDTO(BaseModel):
    username: str
    password: str
    email: str
    is_admin: bool = False
    permissions: list[str] | None = None


class AccessTokenDTO(BaseModel):
    access_token: str


class RefreshTokenDTO(AccessTokenDTO):
    refresh_token: str


class UserLoginDTO(BaseModel):
    username: str
    password: str
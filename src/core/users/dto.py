from pydantic import BaseModel


class UserDTO(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool
    permissions: list[str] | None = (None,)


class UserCreateDTO(BaseModel):
    username: str
    password: str
    email: str
    is_admin: bool
    permissions: list[str] | None = None


class AccessTokenDTO(BaseModel):
    access_token: str


class RefreshTokenDTO(AccessTokenDTO):
    refresh_token: str

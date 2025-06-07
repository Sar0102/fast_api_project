from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from jose import JWTError
from starlette import status

from core.users.dto import UserDTO
from core.users.exceptions import TokenIsNotValidException
from core.users.services import UserService
from infrastructure.database.uow import UnitOfWork


async def get_current_user(
    uow: Annotated[UnitOfWork, Depends(UnitOfWork)],
    token: str = Depends(APIKeyHeader(name="Authorization", auto_error=False)),
) -> UserDTO | None:
    if not token:
        return None
    try:
        user = await UserService.get_current_user(uow, token)
        if not user:
            raise TokenIsNotValidException()
        return UserDTO(
            username=user.username,
            password=user.password,
            email=user.email,
            is_admin=user.is_admin,
            permissions=user.permissions,
        )
    except (JWTError, TokenIsNotValidException) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


def check_permissions(required_permissions: list[str]):
    def permission_dependency(current_user=Depends(get_current_user)):
        user_permissions = current_user.permissions
        # all required permissions in user permissions
        if not set(required_permissions).issubset(set(user_permissions)):
            raise HTTPException(status_code=401, detail="Not enough permissions!")
        return current_user

    return permission_dependency


def context_dependency(
    current_user: str = Depends(get_current_user), uow: UnitOfWork = Depends(UnitOfWork)
):
    return {"current_user": current_user, "uow": uow}

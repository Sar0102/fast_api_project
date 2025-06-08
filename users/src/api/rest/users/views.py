from datetime import timedelta
from typing import Annotated

from fastapi import HTTPException, Depends

from fastapi import APIRouter
from jose import JWTError
from starlette import status

from api.rest import responses
from api.rest.users.decorators import handle_user_errors
from core.users.dto import UserCreateDTO, UserDTO, RefreshTokenDTO, AccessTokenDTO, UserLoginDTO
from dependencies import get_current_user
from core.permissions import Permissions
from core.users.services import (
    UserService,
    ACCESS_TOKEN_EXPIRES_MINUTES,
    REFRESH_TOKEN_EXPIRES_MINUTES,
)
from core.users.exceptions import TokenIsNotValidException
from infrastructure.database.uow import UnitOfWork
from infrastructure.loging_configs.local import logger

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/permissions")
async def get_permissions() -> list[str]:
    """
    Get all available permissions.
    """
    return Permissions.list()


@user_router.post(path="/register", responses={**responses.ObjectCreatedResponse.docs()})
@handle_user_errors
async def create_user(
        uow: Annotated[UnitOfWork, Depends(UnitOfWork)],
        create_dto: UserCreateDTO,
):
    object_id = await UserService.add(
        uow=uow,
        create_dto=create_dto,
    )
    return responses.ObjectCreatedResponse.response(_detail={"id": object_id})


@user_router.get("/")
async def get_users(
        uow: Annotated[UnitOfWork, Depends(UnitOfWork)],
) -> list[UserDTO]:
    return await UserService.get_all(uow)


@user_router.post("/login")
async def login(
        uow: Annotated[UnitOfWork, Depends(UnitOfWork)],
        login_dto: UserLoginDTO
) -> RefreshTokenDTO:
    user = await UserService.authenticate_user(uow, login_dto.username, login_dto.password)
    if not user:
        logger.error("User authentication failed for username: %s", login_dto.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password or username"
        )
    logger.info("User authenticated successfully: %s", login_dto.username)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRES_MINUTES)
    access_token = UserService.create_token(
        data={"sub": login_dto.username, "type": "access"}, expires_delta=access_token_expires
    )
    refresh_token = UserService.create_token(
        data={"sub": login_dto.username, "type": "refresh"}, expires_delta=refresh_token_expires
    )

    return RefreshTokenDTO(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@user_router.post("/refresh")
def refresh_access_token(refresh_token: str) -> AccessTokenDTO:
    try:
        username = UserService.verify_token(refresh_token, "refresh")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
        access_token = UserService.create_token(
            data={"sub": username, "type": "access"}, expires_delta=access_token_expires
        )
        return AccessTokenDTO(access_token=access_token)
    except (TokenIsNotValidException, JWTError) as e:
        raise HTTPException(status_code=401, detail=str(e))


@user_router.get("/me")
async def me(current_user=Depends(get_current_user)) -> UserDTO:
    return current_user

import datetime
from typing import Any

import bcrypt
from jose import jwt
from jose.constants import ALGORITHMS

from infrastructure.database.exceptions import UnitOfWorkError
from infrastructure.database.uow import UnitOfWork
from .dto import UserCreateDTO, UserDTO
from .entities import AdminUser, RegularUser
from .exceptions import TokenIsNotValidException, UserAlreadyExistsException, ServiceError

SECRET_KEY = "super_secret"
ALGORITHM = ALGORITHMS.HS256
ACCESS_TOKEN_EXPIRES_MINUTES = 20
REFRESH_TOKEN_EXPIRES_MINUTES = 60


class UserService:
    @classmethod
    async def get_all(cls, uow: UnitOfWork) -> list[UserDTO]:
        async with uow:
            return await uow.user.get_all()

    @classmethod
    async def add(
        cls,
        uow: UnitOfWork,
        create_dto: UserCreateDTO,
    ) -> int:
        username = create_dto.username
        password = create_dto.password
        email = create_dto.email
        is_admin = create_dto.is_admin
        permissions = create_dto.permissions or []

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        if is_admin:
            user = AdminUser(username=username, password=hashed_password, email=email)
        else:
            user = RegularUser(
                username=username, password=hashed_password, email=email, permissions=permissions
            )
        try:
            async with uow:
                existing_user = await uow.user.get_by_username(username)
                if existing_user:
                    raise UserAlreadyExistsException(username)
                obj_id = await uow.user.add(user)
                await uow.commit()
                return obj_id
        except UnitOfWorkError as e:
            raise ServiceError(f"Error from uow: {e}.")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    @classmethod
    async def authenticate_user(
        cls, uow: UnitOfWork, username: str, password: str
    ) -> UserDTO | None:
        async with uow:
            user = await uow.user.get_by_username(username)
            if not user or not cls.verify_password(password, str(user.password)):
                return None
            return user

    @staticmethod
    def create_token(data: dict[str, Any], expires_delta: datetime.timedelta) -> str:
        payload = data.copy()
        expire = datetime.datetime.now(datetime.UTC) + expires_delta
        payload.update({"exp": expire})
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @classmethod
    async def get_current_user(cls, uow: UnitOfWork, token: str) -> UserDTO | None:
        async with uow:
            username = cls.verify_token(token, token_type="access")
            user = await uow.user.get_by_username(username)
            delattr(user, "password")
            return user

    @staticmethod
    def verify_token(token: str, token_type: str):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        current_toke_type = payload.get("type")
        if current_toke_type != token_type:
            raise TokenIsNotValidException()
        return payload.get("sub")

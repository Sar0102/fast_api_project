
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from core.users.dto import UserDTO
from core.users.entities import BaseUser
from infrastructure.models.user import UserModel


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_username(self, username: str) -> UserDTO | None:
        stmt = select(UserModel).where(UserModel.username == username)
        result = await self.session.execute(stmt)

        row = result.scalar_one_or_none()
        if row is None:
            return None
        return UserDTO(
            id=row.id,
            username=row.username,
            email=row.email,
            is_admin=row.is_admin,
            permissions=row.permissions,
            password=row.password,
        )

    async def get_all(self) -> list[UserDTO]:
        stmt = select(UserModel)
        result = await self.session.execute(stmt)
        return [
            UserDTO(
                id=user.id,
                username=user.username,
                email=user.email,
                is_admin=user.is_admin,
                permissions=user.permissions,
            )
            for user in result.scalars()
        ]

    async def add(self, user: BaseUser) -> int:
        user = UserModel(
            username=user.username,
            password=user.password,
            email=user.email,
            is_admin=user.is_admin,
            permissions=user.permissions,
        )
        stmt = (
            insert(UserModel)
            .values(
                username=user.username,
                password=user.password,
                email=user.email,
                is_admin=user.is_admin,
                permissions=user.permissions,
            )
            .returning(UserModel.id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

from typing import Protocol, Type

from core.users.entities import BaseUser
from infrastructure.models.user import UserModel


class IUserRepository(Protocol):
    def get_by_username(self, username: str) -> UserModel | None:
        ...

    def get_all(self) -> list[Type[UserModel]]:
        ...

    def add(self, user: BaseUser) -> int:
        ...

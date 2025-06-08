import logging
from typing import NoReturn

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.base import engine_manager
from config import settings
from infrastructure.repositories.user import UserRepository

db_settings = settings


class UnitOfWork:
    user: UserRepository

    def init_repositories(self, session: AsyncSession) -> None:
        self.user = UserRepository(session)

    def __init__(
        self,
    ) -> None:
        self.logger = logging.getLogger(__name__)

        self.engine, self.session_factory = engine_manager.get_engine(db_settings.database_url)

        self._session = None
        self._session_nesting_level = 0

    @property
    def session(self) -> AsyncSession:
        if self._session is None:
            raise RuntimeError(
                "An attempt to access the session was unsuccessful. Maybe you forgot to initialize it "
                "via __aenter__ (async with uow)",
            )
        return self._session

    async def __aenter__(self) -> None:
        """Call when entering the context manager."""
        self._session_nesting_level += 1
        if self._session_nesting_level == 1:  # if session is not initialized
            self._session = self.session_factory()
            self.init_repositories(self._session)

    async def __aexit__(self, *args: object) -> None:
        """Call when exiting the context manager."""
        if (
            self._session_nesting_level == 1 and self._session is not None
        ):  # if session is initialized
            await self.rollback()
        self._session_nesting_level -= 1

    async def commit(self) -> None:
        if self._session_nesting_level == 1:
            await self.session.commit()
            await self.session.close()
            self._session = None

    async def rollback(self) -> None:
        if self._session_nesting_level == 1:
            await self.session.rollback()
            await self.session.close()
            self._session = None

    def __getattr__(self, item: str) -> NoReturn:
        """Call when the attribute is not found in the object."""
        raise AttributeError(
            f"Attribute {item} not found. If you want to access the repository, "
            f"you need to initialize it via __aenter__ (async with uow)",
        )

import asyncio
from typing import Callable

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class EnginesManager:
    def __init__(self):
        self._engines: dict[str, AsyncEngine] = {}

    async def dispose_all(self):
        tasks = [engine.dispose() for engine in self._engines.values()]
        await asyncio.gather(*tasks)

    def get_engine(self, dsn: str) -> tuple[AsyncEngine, Callable]:
        try:
            engine = self._engines[dsn]
        except KeyError:
            engine = create_async_engine(
                url=self._check_dsn(dsn),
                echo=False,
            )
            self._engines[dsn] = engine
        return engine, self._create_sessionmaker(engine)

    @staticmethod
    def _create_sessionmaker(engine: AsyncEngine) -> Callable:
        return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @staticmethod
    def _check_dsn(dsn: str) -> str:
        if dsn is None:
            raise ValueError("Invalid DSN")
        if "postgresql" not in dsn:
            raise ValueError("DSN is not valid: postgresql is required. Your DSN: " + dsn)
        if "asyncpg" not in dsn:
            raise ValueError("DSN is not valid: asyncpg driver is required. Your DSN: " + dsn)
        return dsn


engine_manager = EnginesManager()

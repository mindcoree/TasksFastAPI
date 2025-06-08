from asyncio import current_task
from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)
from .config import settings


class DataBaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        max_overflow: int = 10,  # КОЛИЧЕСТВО СЕССИИ
        pool_size: int = 5,  # количество соединений в пуле
    ):
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            max_overflow=max_overflow,
            pool_size=pool_size,
        )

        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine, autoflush=False, expire_on_commit=False
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


db_helper = DataBaseHelper(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    max_overflow=settings.db.max_overflow,
    pool_size=settings.db.pool_size,
)


SessionDep = Annotated[AsyncSession, Depends(db_helper.session_getter)]


def get_scoped_session():
    session = async_scoped_session(
        session_factory=db_helper.session_factory, scopefunc=current_task
    )
    return session


async def scoped_session_dependency() -> AsyncSession:
    session = get_scoped_session()
    yield session
    await session.remove()

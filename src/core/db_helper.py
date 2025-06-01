from typing import AsyncGenerator, Annotated
from .config import settings
from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)


class DatabaseHelper:
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
            pool_size=pool_size,
            max_overflow=max_overflow,
        )

        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,  # Данные сохраняются в памяти после commit
        )

    # Не обязательно делать. Закрывает соединения и удаляет пул.
    # При работе с uvicorn это делается автоматически, но для graceful shutdown — полезно.
    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)

SessionDep = Annotated[AsyncSession, Depends(db_helper.session_getter)]

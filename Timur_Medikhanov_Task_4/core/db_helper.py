from typing import AsyncGenerator, Annotated
from .config import settings
from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = True,
    ):

        self.engine: AsyncEngine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
        )

    async def dispose(self):
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    url=str(settings.db.url),
    echo=settings.db.echo,
)

SessionDep = Annotated[AsyncSession, Depends(db_helper.session_getter)]

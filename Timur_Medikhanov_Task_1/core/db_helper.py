from Timur_Medikhanov_Task_1.core.config import settings
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
    ):
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
        )

        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
        )

    def session_getter(self):
        async with self.session_factory() as session:
            yield session

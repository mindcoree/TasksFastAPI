from typing import Generic, TypeVar, Sequence, Any

from sqlalchemy import select, Result, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: type[T]):
        self.session: AsyncSession = session
        self.model: type[T] = model

    async def get_by_id(self, id_: int) -> T | None:
        stmt = select(self.model).where(self.model.id == id_)
        result: Result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, kwargs: dict) -> T:
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        return instance

    async def update_by_id(self, id_: int, kwargs: dict) -> T | None:
        stmt = (
            update(self.model)
            .where(self.model.id == id_)
            .values(**kwargs)
            .returning(self.model)
        )
        result: Result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def delete_by_(self, column_name: str, value: Any) -> int | None:
        column = getattr(self.model, column_name)
        stmt = delete(self.model).where(column == value).returning(self.model.id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def filter_by(self, kwargs: dict) -> Sequence[T]:
        stmt = select(self.model).filter_by(**kwargs)
        result: Result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_paginated(self, offset: int, limit: int) -> Sequence[T]:
        stmt = select(self.model).offset(offset).limit(limit)
        result: Result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_instance_by_(self, column_name: str, value: Any) -> T | None:
        column = getattr(self.model, column_name)
        stmt = select(self.model).where(column == value)
        result: Result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class BaseAuthRepository(BaseRepository[T], Generic[T]):
    def __init__(self, session: AsyncSession, model: type[T]):
        super().__init__(session=session, model=model)

    async def get_by_login(self, login: str) -> T | None:
        return await self.get_instance_by_("login", value=login)

    async def get_by_email(self, email: str) -> T | None:
        return await self.get_instance_by_("email", value=email)

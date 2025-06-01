from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from utils import auth
from .schemas import ResponseUser, UserCreate, AccessToken, UserLogin
from .models import User


class UserRepository:
    def __init__(self, session):
        self.session: AsyncSession = session

    async def get_users(self) -> Sequence[User]:
        stms = select(User)
        result = await self.session.scalars(stms)
        return result.all()

    async def create_user(self, user_in: UserCreate) -> User:
        create_user = User(**user_in.model_dump())
        self.session.add(create_user)
        await self.session.commit()
        await self.session.refresh(create_user)
        return create_user

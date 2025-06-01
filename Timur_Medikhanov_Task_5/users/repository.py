from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from utils import auth
from .schemas import ResponseUser, UserCreate, UserLogin
from .models import User


class UserRepository:
    def __init__(self, session):
        self.session: AsyncSession = session

    async def get_user(self, get_user: UserLogin) -> User:
        users = select(User).where(User.username == get_user.username)
        result: Result = await self.session.execute(users)
        user = result.scalars().one_or_none()
        return user

    async def create(self, username: str, password_hash: str) -> User:
        new_user = User(username=username, password=password_hash)
        self.session.add(new_user)
        await self.session.commit()
        return new_user

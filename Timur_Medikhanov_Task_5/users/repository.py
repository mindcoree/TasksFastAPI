from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from .schemas import UserLogin
from .models import User, Role


class UserRepository:
    def __init__(self, session):
        self.session: AsyncSession = session

    async def get_user(self, get_user: UserLogin) -> User:
        users = select(User).where(User.username == get_user.username)
        result: Result = await self.session.execute(users)
        user = result.scalars().one_or_none()
        return user

    async def create(self, username: str, password_hash: str) -> User:
        new_user = User(username=username, password=password_hash, role=Role.user)
        self.session.add(new_user)
        await self.session.commit()
        return new_user

    async def get_user_by_id(self, user_id) -> User:
        return await self.session.get(User, user_id)

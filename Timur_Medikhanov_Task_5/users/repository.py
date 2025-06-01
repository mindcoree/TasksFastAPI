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

    async def create_users(self, user_in: UserCreate) -> ResponseUser:
        hash_password = auth.hash_password(user_in.password)
        new_user = User(username=user_in.username, password=hash_password)
        self.session.add(new_user)
        await self.session.commit()
        return ResponseUser(id=new_user.id, username=new_user.username)

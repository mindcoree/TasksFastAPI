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


async def create_users(session: AsyncSession, user_in: UserCreate) -> ResponseUser:
    hash_password = auth.hash_password(user_in.password)
    new_user = User(username=user_in.username, password=hash_password)
    session.add(new_user)
    await session.commit()
    return ResponseUser(id=new_user.id, username=new_user.username)


async def sign_in(user_login: ResponseUser) -> AccessToken:
    payload = {
        "sub": str(user_login.id),
        "username": user_login.username,
    }
    token = auth.encode_jwt(payload=payload)
    return AccessToken(token=token, token_type="Cookie")


async def get_user(session: AsyncSession, user: UserLogin) -> User:
    users = select(User).where(User.username == user.username)
    result: Result = await session.execute(users)
    user = result.scalars().first()
    return user

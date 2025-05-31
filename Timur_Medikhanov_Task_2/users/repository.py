from sqlalchemy import select, Result
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from utils import auth
from .schemas import UserLogin, ResponseUser, UserCreate
from .models import User


async def create_users(session: AsyncSession, user_in: UserCreate) -> ResponseUser:
    hash_password = auth.hash_password(user_in.password)
    new_user = User(username=user_in.username, password=hash_password)
    session.add(new_user)
    await session.commit()
    return ResponseUser(id=new_user.id, username=new_user.username)


async def sign_in(session: AsyncSession, sign_in_user: UserLogin) -> dict:
    users = select(User).where(User.username == sign_in_user.username)
    result: Result = await session.execute(users)
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The user is unauthorized",
        )

    verify_password = auth.verify_password(
        password=sign_in_user.password,
        hashed_password=user.password,
    )

    if not verify_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not the right password",
        )

    return {
        "complete": True,
        "message": "The user is authorized",
    }

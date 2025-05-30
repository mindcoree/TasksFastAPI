from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import UserLogin, ResponseUser, UserCreate
from .dependencies import CheckUniqueUsers
from .models import User
from sqlalchemy import select, Result


async def create_users(
    session: AsyncSession, user_in: CheckUniqueUsers
) -> ResponseUser:
    new_user = User(**user_in.model_dump())
    session.add(new_user)
    await session.commit()
    return ResponseUser(id=new_user.id, username=new_user.username)


async def get_users(session: AsyncSession, get_user: UserLogin) -> dict:
    users = select(User).where(get_user.password == User.password)
    result: Result = await session.execute(users)
    check_auth = result.scalars().first()
    if not check_auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The user is unauthorized",
        )
    return {
        "complete": True,
        "message": "The user is authorized",
    }

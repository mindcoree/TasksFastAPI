from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from users.schemas import UserCreate
from sqlalchemy import select, Result
from .models import User
from fastapi import HTTPException, status


async def check_unique_user(
    session: AsyncSession, check_user: UserCreate
) -> UserCreate:
    users = select(User).where(check_user.username == User.username)
    result: Result = await session.execute(users)
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username has already been taken.",
        )
    return check_user


CheckUniqueUsers = Annotated[UserCreate, Depends(check_unique_user)]

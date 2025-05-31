from typing import Annotated
from fastapi import Depends

from users.schemas import UserCreate, UserLogin, ResponseUser
from sqlalchemy import select, Result

from utils import auth
from .models import User
from fastapi import HTTPException, status
from core.db_helper import SessionDep


async def check_unique_user(session: SessionDep, check_user: UserCreate) -> UserCreate:
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


async def verify_credentials(session: SessionDep, sign_in_user: UserLogin) -> UserLogin:
    users = select(User).where(User.username == sign_in_user.username)
    result: Result = await session.execute(users)
    user = result.scalars().first()

    if not user or not auth.verify_password(
        password=sign_in_user.password,
        hashed_password=user.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return user


VerificationUser = Annotated[ResponseUser, Depends(verify_credentials)]

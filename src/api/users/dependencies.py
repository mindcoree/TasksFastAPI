from .repository import UserRepository
from .service import UserService
from typing import Annotated
from fastapi import Depends, Form, HTTPException, status, Request
from sqlalchemy import select, Result
from .schemas import UserCreate, UserLogin, ResponseUser
from utils import auth
from .models import User
from core.db_helper import SessionDep
from jwt.exceptions import InvalidTokenError
from api.users import repository as repo


def get_user_service(session: SessionDep) -> UserService:
    repos = UserRepository(session)
    return UserService(repository=repos)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


async def check_unique_user(
    session: SessionDep,
    check_user: Annotated[UserCreate, Form()],
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


async def verify_credentials(
    session: SessionDep, sign_in_user: Annotated[UserLogin, Form()]
) -> UserLogin:
    user = await repo.get_user(session=session, user=sign_in_user)
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


async def get_current_user(request: Request) -> ResponseUser:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No token provided",
        )
    try:
        payload = auth.decode_jwt(token=token)
        return ResponseUser(id=payload["sub"], username=payload["username"])
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


CurrentUser = Annotated[ResponseUser, Depends(get_current_user)]

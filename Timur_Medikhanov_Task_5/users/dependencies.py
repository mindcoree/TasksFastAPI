from typing import Annotated
from fastapi import Depends, Form, Request
from .schemas import UserCreate, UserLogin, ResponseUser
from .services import UserAuthService
from .repository import UserRepository
from core.db_helper import SessionDep


def get_user_auth_service(session: SessionDep) -> UserAuthService:
    repository = UserRepository(session=session)
    return UserAuthService(repository=repository)


UserAuthServiceDep = Annotated[UserAuthService, Depends(get_user_auth_service)]


async def check_unique_user(
    check_user: Annotated[UserCreate, Form()],
    user_auth_service: UserAuthServiceDep,
) -> UserCreate:
    return await user_auth_service.check_unique_user(check_user=check_user)


CheckUniqueUsers = Annotated[UserCreate, Depends(check_unique_user)]


async def verify_credentials(
    sign_in_user: Annotated[UserLogin, Form()],
    user_auth_service: UserAuthServiceDep,
) -> ResponseUser:
    return await user_auth_service.verify_credentials(sign_in_user=sign_in_user)


VerificationUser = Annotated[ResponseUser, Depends(verify_credentials)]


def get_current_user(
    request: Request,
    user_auth_service: UserAuthServiceDep,
) -> ResponseUser:
    return user_auth_service.get_current_user(request=request)


CurrentUser = Annotated[ResponseUser, Depends(get_current_user)]

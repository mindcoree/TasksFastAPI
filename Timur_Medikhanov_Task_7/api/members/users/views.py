from typing import Annotated

from fastapi import APIRouter, status, Response, Form
from core.config import settings
from .schemas import TokenInfo, UserCreate, UserInfo, UserCredentials
from .dependencies import (
    UserAuthServiceDep,
    UserRestricted,
    UserAuthValidatorDep,
)
from utils import auth

router = APIRouter(prefix=settings.api.members.users.prefix, tags=["Users"])


@router.post("/login", response_model=TokenInfo)
async def login(
    credentials: Annotated[UserCredentials, Form()],
    validation: UserAuthValidatorDep,
    response: Response,
) -> TokenInfo:
    user = await validation.verify_credentials(credentials)
    access_token = await auth.create_access_token(user_info=user)
    refresh_token = await auth.create_refresh_token(user_info=user)
    await auth.set_token_cookie(
        response=response,
        key="access_token",
        value=access_token,
        max_age=settings.auth.access_expire_min * 60,
    )
    await auth.set_token_cookie(
        response=response,
        key="refresh_token",
        value=refresh_token,
        max_age=settings.auth.refresh_expire_days * 24 * 60,  # * 60 для тест
    )
    return TokenInfo(access=access_token, refresh=refresh_token)


@router.post(
    "/register",
    response_model=UserInfo,
    status_code=status.HTTP_201_CREATED,
)
async def user_register(
    auth_user_service: UserAuthServiceDep,
    validation: UserAuthValidatorDep,
    registration: Annotated[UserCreate, Form()],
) -> UserInfo:
    validation.validate_create(data=registration)
    return await auth_user_service.create_user(user_in=registration)


@router.get("/info_user", response_model=UserInfo)
async def info_user(auth_service: UserAuthServiceDep, current_user: UserRestricted):
    user_id = int(current_user.get("sub"))
    return await auth_service.get_by_id(user_id)

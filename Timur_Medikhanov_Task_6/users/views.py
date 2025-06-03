from fastapi import APIRouter, status, Response
from core.config import settings
from .schemas import TokenInfo, UserScheme, AdminScheme
from .dependencies import VerifiedUser
from .dependencies import (
    CheckUniqueUser,
    UserAuthServiceDep,
    CurrentUser,
    CurrentAdmin,
)
from utils import auth

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/login", response_model=TokenInfo)
async def login(
    credentials: VerifiedUser,
    user_auth_service: UserAuthServiceDep,
    response: Response,
) -> TokenInfo:
    user_login: TokenInfo = await user_auth_service.sign_in(user_login=credentials)
    await auth.set_token_cookie(
        response=response,
        key="access_token",
        value=user_login.access,
        max_age=settings.auth.access_token_expire_min * 60,
    )
    await auth.set_token_cookie(
        response=response,
        key="refresh_token",
        value=user_login.refresh,
        max_age=settings.auth.refresh_token_expire_days * 24 * 60 * 60,
    )
    return user_login


@router.post(
    "/register",
    response_model=UserScheme,
    status_code=status.HTTP_201_CREATED,
)
async def user_register(
    auth_user_service: UserAuthServiceDep,
    reg_user: CheckUniqueUser,
):

    return await auth_user_service.create_user(user=reg_user)


@router.get("/user/info-me", response_model=UserScheme)
async def info_user(user_auth_service: UserAuthServiceDep, current_user: CurrentUser):
    user_id = int(current_user.get("sub"))
    return await user_auth_service.get_user(user_id)


@router.post(
    "/create/admin",
    response_model=AdminScheme,
    status_code=status.HTTP_201_CREATED,
)
async def create_admin(
    user_auth_service: UserAuthServiceDep, admin_info: CheckUniqueUser
):
    return await user_auth_service.create_admin(admin_info=admin_info)


@router.get("/admin/users", response_model=list[UserScheme])
async def users_list(
    current_admin: CurrentAdmin, user_auth_service: UserAuthServiceDep
):

    return await user_auth_service.get_list_user()

from fastapi import (
    APIRouter,
    Response,
    status,
    Request,
    HTTPException,
)
from .dependencies import (
    UserAuthServiceDep,
    VerificationUser,
    CheckUniqueUsers,
    CurrentUser,
    CurrentAdmin,
)
from core.config import settings
from utils import auth
from .schemas import TokenInfo, UserSchemas, UserPayload

router = APIRouter()


@router.post("/login", response_model=TokenInfo)
async def login(
    credentials: VerificationUser,
    user_auth_service: UserAuthServiceDep,
    response: Response,
) -> TokenInfo:
    user_login = await user_auth_service.sign_in(user_login=credentials)
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
    response_model=UserSchemas,
    status_code=status.HTTP_201_CREATED,
)
async def user_register(
    reg_user: CheckUniqueUsers,
    user_auth_service: UserAuthServiceDep,
):
    return await user_auth_service.create_user(user_in=reg_user)


@router.get("/me", response_model=UserPayload)
async def info_user(current_user: CurrentUser):
    return UserPayload(**current_user)


@router.get("/me/admin", response_model=UserPayload)
async def info_user(current_admin: CurrentAdmin):
    return UserPayload(**current_admin)

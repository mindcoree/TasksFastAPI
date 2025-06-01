from fastapi import APIRouter, Response, status
from .schemas import AccessToken, ResponseUser
from .dependencies import (
    UserAuthServiceDep,
    VerificationUser,
    CheckUniqueUsers,
    CurrentUser,
)

router = APIRouter()


@router.post("/login", response_model=AccessToken)
async def login(
    credentials: VerificationUser,
    response: Response,
    user_auth_service: UserAuthServiceDep,
):
    access_token = await user_auth_service.sign_in(user_login=credentials)

    response.set_cookie(
        key="access_token",
        value=access_token.token,
        samesite="lax",
        secure=False,
        httponly=True,
        max_age=30 * 60,
    )

    return access_token


@router.post(
    "/register",
    response_model=ResponseUser,
    status_code=status.HTTP_201_CREATED,
)
async def user_register(
    reg_user: CheckUniqueUsers,
    user_auth_service: UserAuthServiceDep,
):
    return await user_auth_service.create_user(user_in=reg_user)


@router.get("/me", response_model=ResponseUser)
async def info_user(current_user: CurrentUser):
    return current_user

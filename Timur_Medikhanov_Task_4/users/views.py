from fastapi import APIRouter, status, Response
from core.db_helper import SessionDep
from users import repository as repo
from .schemas import ResponseUser, AccessToken
from .dependencies import VerificationUser
from .dependencies import CheckUniqueUsers

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/login", response_model=AccessToken)
async def login(credentials: VerificationUser, response: Response):
    access_token = await repo.sign_in(user_login=credentials)

    response.set_cookie(
        key="access_token",
        value=access_token.token,
        httponly=True,  # Защита от доступа через JavaScript
        secure=True,  # Только для HTTPS
        samesite="lax",  # Защита от CSRF
        max_age=30 * 60,
    )

    return access_token


@router.post(
    "/register",
    response_model=ResponseUser,
    status_code=status.HTTP_201_CREATED,
)
async def user_register(session: SessionDep, reg_user: CheckUniqueUsers):
    return await repo.create_users(session=session, user_in=reg_user)

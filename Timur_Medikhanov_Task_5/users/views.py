from fastapi import APIRouter, status, Response
from core.db_helper import SessionDep
from users import repository as repo
from .schemas import ResponseUser, AccessToken
from .dependencies import VerificationUser, CheckUniqueUsers, CurrentUser


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/login", response_model=AccessToken)
async def login(credentials: VerificationUser, response: Response):
    access_token = await repo.sign_in(user_login=credentials)

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
async def user_register(session: SessionDep, reg_user: CheckUniqueUsers):
    return await repo.create_users(session=session, user_in=reg_user)


@router.get("/me", response_model=ResponseUser)
async def info_user(session: SessionDep, current_user: CurrentUser):
    user = await repo.get_user(session=session, user=current_user)
    return ResponseUser(id=user.id, username=user.username)

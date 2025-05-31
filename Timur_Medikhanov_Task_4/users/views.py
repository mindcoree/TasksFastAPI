from fastapi import APIRouter, status
from core.db_helper import SessionDep
from users import repository as repo
from .schemas import ResponseUser, AccessToken
from .dependencies import VerificationUser
from .dependencies import CheckUniqueUsers

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/login", response_model=AccessToken)
async def login(credentials: VerificationUser):
    return await repo.sign_in(user_login=credentials)


@router.post(
    "/register",
    response_model=ResponseUser,
    status_code=status.HTTP_201_CREATED,
)
async def user_register(session: SessionDep, reg_user: CheckUniqueUsers):
    return await repo.create_users(session=session, user_in=reg_user)

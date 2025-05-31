from fastapi import APIRouter, status
from core.db_helper import SessionDep
from users import repository as repo
from .schemas import UserLogin, UserCreate, ResponseUser
from .models import User
from .dependencies import CheckUniqueUsers

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/login")
async def user_login(session: SessionDep, user: UserLogin):
    return await repo.sign_in(session=session, sign_in_user=user)


@router.post(
    "/register",
    response_model=ResponseUser,
    status_code=status.HTTP_201_CREATED,
)
async def user_register(session: SessionDep, reg_user: CheckUniqueUsers):
    return await repo.create_users(session=session, user_in=reg_user)

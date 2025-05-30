from fastapi import APIRouter
from core.db_helper import SessionDep
from users import repository as repo
from .schemas import UserLogin, UserCreate, ResponseUser
from .models import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/login")
async def user_login(session: SessionDep, user: UserLogin):
    return await repo.get_users(session=session, get_user=user)


@router.post("/register", response_model=ResponseUser)
async def user_register(session: SessionDep, reg_user: UserCreate):
    return await repo.create_users(session=session, user_in=reg_user)

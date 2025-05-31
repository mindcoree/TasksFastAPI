from typing import Sequence

from fastapi import APIRouter, status
from .dependencies import UserServiceDep
from .schemas import UserRead, UserCreate


router = APIRouter(tags=["users"])


@router.get("/get-list-users", response_model=list[UserRead])
async def get_users(service: UserServiceDep) -> Sequence[UserRead]:
    users = await service.get_users()
    return users


@router.post(
    "/create-user", response_model=UserCreate, status_code=status.HTTP_201_CREATED
)
async def create_user(service: UserServiceDep, user_in: UserCreate):
    return await service.created_user(user_in=user_in)

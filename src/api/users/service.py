from typing import Sequence

from .repository import UserRepository
from .schemas import UserRead, UserCreate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repo = repository

    async def get_users(self) -> Sequence[UserRead]:
        users = await self.repo.get_users()
        return users

    async def created_user(self, user_in) -> UserCreate:
        create_user = await self.repo.create_user(user_in)
        return create_user

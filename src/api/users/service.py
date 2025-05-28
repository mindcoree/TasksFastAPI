from typing import Sequence

from src.api.users.repository import UserRepository
from src.api.users.schemas import UserRead, UserCraete


class UserService:
    def __init__(self, repository: UserRepository):
        self.repo = repository

    async def get_users(self) -> Sequence[UserRead]:
        users = await self.repo.get_users()
        return users

    async def created_user(self, user_in) -> UserCraete:
        create_user = await self.repo.create_user(user_in)
        return create_user

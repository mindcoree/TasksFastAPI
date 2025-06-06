from api.common.services import BaseAuthService
from api.common.enums import Role
from api.members.models import Members
from .repository import UserAuthRepository
from .schemas import UserCreate


class UserAuthService(BaseAuthService[Members]):
    def __init__(self, repository: UserAuthRepository):
        super().__init__(repository=repository)

    async def create_user(self, user_in: UserCreate) -> Members:
        return await super().create_auth(auth_in=user_in, role=Role.USER)

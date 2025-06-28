from api.common.services import BaseAuthService
from api.common.enums import Role
from api.members.models import Member
from .repository import UserAuthRepository
from .schemas import UserCreate


class UserAuthService(BaseAuthService[Member]):
    def __init__(self, repository: UserAuthRepository):
        super().__init__(repository=repository, model=Member)

    async def create_user(self, user_in: UserCreate) -> Member:
        return await super().create_auth(auth_in=user_in, role=Role.USER)

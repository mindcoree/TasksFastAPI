from api.common.services import BaseAuthService, BaseService
from api.common.enums import Role
from .models import User
from .repository import UserAuthRepository
from .schemas import UserCreate


class UserAuthService(BaseService[User], BaseAuthService[User]):
    def __init__(self, repository: UserAuthRepository):
        super().__init__(repository=repository)

    async def create_user(self, user: UserCreate) -> User:
        return await self.create_auth(auth_in=user, role=Role.USER)

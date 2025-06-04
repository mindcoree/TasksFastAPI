from api.common.services import BaseAuthService
from api.common.enums import Role
from .models import User
from .repository import UserAuthRepository


class UserAuthService(BaseAuthService[User]):
    def __init__(self, repository: UserAuthRepository):
        super().__init__(repository=repository)

    async def create_user(self, user: User) -> User:
        return await super().create(auth_info=user, role=Role.USER)

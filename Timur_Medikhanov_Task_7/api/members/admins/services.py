from api.common.services import BaseAuthService
from .models import Admin
from .repository import AdminAuthRepository
from .schemas import AdminCreate
from api.common.enums import Role


class AdminAuthService(BaseAuthService[Admin]):
    repo: AdminAuthRepository[Admin]

    def __init__(self, repository: AdminAuthRepository[Admin]):
        super().__init__(repository=repository)

    async def create_admin(self, admin: AdminCreate) -> Admin:
        return await super().create(auth_info=admin, role=Role.ADMIN)

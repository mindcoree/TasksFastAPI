from api.common.services import BaseAuthService
from .models import Admin
from .repository import AdminAuthRepository
from .schemas import AdminCreate
from api.common.enums import Role


class AdminAuthService(BaseAuthService[Admin]):
    def __init__(self, repository: AdminAuthRepository):
        super().__init__(repository=repository)

    async def create_admin(self, admin: AdminCreate) -> Admin:
        return await self.create_auth(auth_in=admin, role=Role.ADMIN)

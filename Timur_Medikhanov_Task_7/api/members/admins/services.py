from api.common.enums import Role
from api.common.services import BaseAuthService
from api.members.models import Member
from .repository import AdminAuthRepository
from .schemas import AdminCreate


class AdminAuthService(BaseAuthService[Member]):
    def __init__(self, repository: AdminAuthRepository):
        super().__init__(repository=repository, model=Member)

    async def create_admin(self, admin_in: AdminCreate) -> Member:
        return await self.create_auth(auth_in=admin_in, role=Role.ADMIN)

    async def get_admin_by_id(self, admin_id: int):
        return await self.repo.get_instance_by_("id", value=admin_id)

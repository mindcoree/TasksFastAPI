from sqlalchemy.ext.asyncio import AsyncSession

from api.common.repository import BaseAuthRepository, BaseRepository
from api.members.models import Member


class AdminAuthRepository(BaseAuthRepository[Member]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Member)


class AdminRepository(BaseRepository[Member]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Member)

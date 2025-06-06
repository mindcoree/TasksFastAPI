from sqlalchemy.ext.asyncio import AsyncSession
from api.common.repository import BaseAuthRepository, BaseRepository
from api.members.models import Members


class AdminAuthRepository(BaseAuthRepository[Members]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Members)


class AdminRepository(BaseRepository[Members]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Members)

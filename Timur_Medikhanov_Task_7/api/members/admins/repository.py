from sqlalchemy.ext.asyncio import AsyncSession
from .models import Admin
from api.common.repository import BaseAuthRepository, BaseRepository


class AdminAuthRepository(BaseAuthRepository[Admin]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Admin)


class AdminRepository(BaseRepository[Admin]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Admin)

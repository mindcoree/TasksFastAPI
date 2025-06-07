from sqlalchemy.ext.asyncio import AsyncSession

from api.common.repository import BaseAuthRepository
from api.members.models import Member


class UserAuthRepository(BaseAuthRepository[Member]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Member)

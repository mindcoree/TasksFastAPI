from sqlalchemy.ext.asyncio import AsyncSession

from api.common.repository import BaseAuthRepository
from .models import User


class UserAuthRepository(BaseAuthRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

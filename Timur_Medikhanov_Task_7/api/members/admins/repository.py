from sqlalchemy.ext.asyncio import AsyncSession
from .models import Admin
from api.common.repository import BaseAuthRepository


class AdminAuthRepository(BaseAuthRepository[Admin]):
    def __init__(self, session: AsyncSession, model: type[Admin] = Admin):
        super().__init__(session, model)

    async def create(self, **kwargs) -> Admin:
        return await super().create(**kwargs)

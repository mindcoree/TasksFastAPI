from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.common.repository import BaseRepository
from .models import Product


class ProductRepository(BaseRepository[Product]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Product)

    async def get_list_products(self):
        stmt = select(Product).order_by(Product.id)
        result: Result = await self.session.execute(stmt)
        return result.scalars().all()

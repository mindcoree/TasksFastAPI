from typing import Any, Sequence

from sqlalchemy import select, Result, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from api.common.repository import BaseRepository
from .models import Product
from ..common.pagination import PaginationProduct


class ProductRepository(BaseRepository[Product]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Product)

    async def products_list_with_pagination(
        self, pagination: PaginationProduct
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        stmt = (
            select(Product)
            .order_by(Product.id)
            .offset(pagination.offset)
            .limit(pagination.limit)
        )
        result: Result = await self.session.execute(stmt)
        return result.scalars().all()

    async def product_by_id(self, id_product: int) -> Product | None:
        stmt = select(Product).where(Product.id == id_product)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

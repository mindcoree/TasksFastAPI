from typing import Any, Coroutine, Sequence

from fastapi import HTTPException, status
from sqlalchemy import Row, RowMapping
from sqlalchemy.exc import IntegrityError

from api.common.services import BaseService
from .exceptions import ProductNotFoundId, InvalidProductData, ProductAlreadyExists
from .models import Product
from .repository import ProductRepository
from .schemas import ProductIn, ProductUpdate
from ..common.pagination import PaginationProduct


class ProductService(BaseService[Product]):
    repo: ProductRepository

    def __init__(self, repository: ProductRepository):
        super().__init__(repository=repository, model=Product)

    async def create_product(self, product_in: ProductIn) -> Product:
        if product_in.price <= 0 or product_in.stock < 0:
            raise InvalidProductData("price or stock must be positive")
        try:
            product = await self.repo.create(product_in.model_dump())
        except IntegrityError:
            raise ProductAlreadyExists(name=product_in.name)

        return product

    async def get_product_by_id(self, product_id: int) -> Product:
        product = await self.repo.get_by_id(product_id)
        return await self.commit_or_raise(
            result=product,
            http_exception=ProductNotFoundId(product_id),
            commit=False,
        )

    async def get_list_products_with_pagination(
        self, pagination: PaginationProduct
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        list_products = await self.repo.products_list_with_pagination(pagination)
        if not list_products:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There are not products",
            )
        return list_products

    async def update_product_by_id(
        self, product_id: int, product_in: ProductUpdate, partial: bool = False
    ) -> Product:
        price = product_in.price
        stock = product_in.stock
        if price is not None and price <= 0 or stock is not None and stock < 0:
            raise InvalidProductData("price or stock must be positive")
        try:
            updated_product = await self.repo.update_by_id(
                id_=product_id,
                kwargs=product_in.model_dump(exclude_unset=partial),
            )
        except IntegrityError:
            raise ProductAlreadyExists(name=product_in.name)

        return await self.commit_or_raise(
            result=updated_product, http_exception=ProductNotFoundId(product_id)
        )

    async def delete_product_by_id(self, delete_id: int) -> None:
        deleted_product = await self.repo.delete_by_("id", value=delete_id)
        await self.commit_or_raise(
            result=deleted_product,
            http_exception=ProductNotFoundId(delete_id),
        )

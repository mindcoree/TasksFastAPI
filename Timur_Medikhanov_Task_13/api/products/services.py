from typing import Any, Sequence

from fastapi import HTTPException, status
from sqlalchemy import Row, RowMapping
from sqlalchemy.exc import IntegrityError

from api.common.services import BaseService
from .exceptions import ProductNotFoundId, InvalidProductData, ProductAlreadyExists
from .models import Product
from .repository import ProductRepository
from .schemas import ProductIn, ProductUpdate, ProductOut
from ..common.pagination import PaginationProduct
import redis.asyncio as redis


class ProductService(BaseService[Product]):
    repo: ProductRepository
    CACHE_TTL = 300  # 5 minutes

    def __init__(
        self, repository: ProductRepository, redis_client: redis.Redis | None = None
    ):
        super().__init__(repository=repository, model=Product)
        self.redis_client = redis_client

    async def create_product(self, product_in: ProductIn) -> Product:
        if product_in.price <= 0 or product_in.stock < 0:
            raise InvalidProductData("price or stock must be positive")
        try:
            product = await self.repo.create(product_in.model_dump())
        except IntegrityError:
            raise ProductAlreadyExists(name=product_in.name)

        return product

    async def get_product_by_id(self, product_id: int) -> ProductOut:
        cache_key = f"product:{product_id}"
        if self.redis_client:
            try:
                cached_product = await self.redis_client.get(cache_key)
                if cached_product:
                    return ProductOut.model_validate_json(cached_product)
            except redis.RedisError as e:
                print(
                    f"Redis error while fetching product {product_id}: {e},falling back to cache"
                )

        product = await self.repo.get_by_id(product_id)
        product = await self.commit_or_raise(
            result=product,
            http_exception=ProductNotFoundId(product_id),
            commit=False,
        )
        product_out = ProductOut.model_validate(product)
        if self.redis_client:
            try:
                await self.redis_client.setex(
                    cache_key,
                    self.CACHE_TTL,
                    product_out.model_dump_json(),
                )
            except redis.RedisError:
                print(f"Failed to create product {product_id}")

        return product_out

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

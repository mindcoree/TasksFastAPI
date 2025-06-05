from fastapi import HTTPException, status
from api.common.services import BaseService
from .models import Product
from .repository import ProductRepository
from .schemas import ProductIn, ProductUpdate


class ProductService(BaseService[Product]):
    repo: ProductRepository

    def __init__(self, repository: ProductRepository):
        super().__init__(repository=repository)

    async def create_product(self, product_in: ProductIn) -> Product:
        existing = self.repo.get_instance_by_(column_name="name", value=product_in.name)
        await self.ensure_unique(existing, product_in.name)
        if product_in.price < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="price must be positive",
            )

        return await self.repo.create(**product_in.model_dump())

    async def get_product_by_id(self, id_product: int) -> Product:
        return await self.get_by_id(id_instance=id_product)

    async def list_product(self) -> list[Product]:
        return await self.repo.get_list_product()

    async def update_product_by_id(
        self, product_id: int, product_in: ProductUpdate
    ) -> Product:
        return await self.update_by_id(
            id_instance=product_id, **product_in.model_dump()
        )

    async def delete_product_by_id(self, delete_id: int) -> None:
        return self.delete_by_id(delete_id)

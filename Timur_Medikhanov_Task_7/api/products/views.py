from typing import Annotated

from fastapi import APIRouter, status, Form

from api.members.admins.dependencies import AdminRestricted
from core.config import settings
from type.annotated import form_model
from .dependencies import ProductServiceDep, ExistingProduct
from .schemas import ProductOut, ProductIn, ProductUpdatePartial, ProductUpdate

router = APIRouter(prefix=settings.api.products.prefix, tags=["products REST"])


@router.get("/product/{product_id}", response_model=ProductOut)
async def get_product(
    restricted: AdminRestricted,
    product_entity: ExistingProduct,
) -> ProductOut:
    return product_entity


@router.get("/list-products")
async def get_list_products(
    restricted: AdminRestricted,
    service: ProductServiceDep,
) -> list[ProductOut]:
    return await service.get_list_products()


@router.post(
    "/create/product",
    response_model=ProductOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    restricted: AdminRestricted,
    product: Annotated[ProductIn, Form()],
    service: ProductServiceDep,
) -> ProductOut:

    return await service.create_product(product_in=product)


@router.put(
    "/update/{product_id}",
    response_model=ProductOut,
)
async def update_product(
    product_entity: ExistingProduct,
    restricted: AdminRestricted,
    product: form_model(ProductUpdate),
    service: ProductServiceDep,
) -> ProductOut:
    return await service.update_product_by_id(
        product_id=product_entity.id, product_in=product
    )


@router.patch(
    "/update-partial/{product_id}",
    response_model=ProductOut,
)
async def update_product(
    product_entity: ExistingProduct,
    restricted: AdminRestricted,
    product: form_model(ProductUpdatePartial),
    service: ProductServiceDep,
) -> ProductOut:
    return await service.update_product_by_id(
        product_id=product_entity.id, product_in=product, partial=True
    )


@router.delete(
    "/delete/{product_id}",
)
async def delete_product(
    product_entity: ExistingProduct,
    restricted: AdminRestricted,
    service: ProductServiceDep,
) -> dict:
    await service.delete_product_by_id(delete_id=product_entity.id)
    return {"successfully": True}

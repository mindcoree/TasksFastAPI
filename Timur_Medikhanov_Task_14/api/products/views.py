from fastapi import APIRouter, status, Depends

from api.members.admins.dependencies import AdminRestricted
from core.config import settings
from type.annotated import form_model, query_model
from .dependencies import ProductServiceDep
from .schemas import ProductOut, ProductIn, ProductUpdatePartial, ProductUpdate
from ..common.pagination import PaginationProduct

router = APIRouter(prefix=settings.api.products.prefix, tags=["products REST"])


@router.get("/product/{product_id}", response_model=ProductOut)
async def get_product(
    restricted: AdminRestricted,
    product_id: int,
    service: ProductServiceDep,
) -> ProductOut:
    return await service.get_product_by_id(product_id)


@router.get("/list-products")
async def get_list_products(
    restricted: AdminRestricted,
    pagination_product: query_model(PaginationProduct),
    service: ProductServiceDep,
) -> list[ProductOut]:
    return await service.get_list_products_with_pagination(pagination_product)


@router.post(
    "/create/product",
    response_model=ProductOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    restricted: AdminRestricted,
    product: form_model(ProductIn),
    service: ProductServiceDep,
) -> ProductOut:

    return await service.create_product(product_in=product)


@router.put(
    "/update/{product_id}",
    response_model=ProductOut,
)
async def update_product(
    product_id: int,
    restricted: AdminRestricted,
    product: form_model(ProductUpdate),
    service: ProductServiceDep,
) -> ProductOut:
    return await service.update_product_by_id(product_id=product_id, product_in=product)


@router.patch(
    "/update-partial/{product_id}",
    response_model=ProductOut,
)
async def update_product(
    product_id: int,
    restricted: AdminRestricted,
    product: form_model(ProductUpdatePartial),
    service: ProductServiceDep,
) -> ProductOut:
    return await service.update_product_by_id(
        product_id=product_id, product_in=product, partial=True
    )


@router.delete(
    "/delete/{product_id}",
)
async def delete_product(
    product_id: int,
    restricted: AdminRestricted,
    service: ProductServiceDep,
) -> dict:
    await service.delete_product_by_id(delete_id=product_id)
    return {"successfully": True}

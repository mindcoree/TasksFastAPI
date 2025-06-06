from fastapi import APIRouter, status
from core.config import settings
from .dependencies import ProductServiceDep
from .schemas import ProductOut, ProductIn
from type.annotated import form_model
from api.members.admins.dependencies import AdminRestricted


router = APIRouter(prefix=settings.api.products.prefix, tags=["products REST"])


@router.get("/product/{product_id}", response_model=ProductOut)
async def get_product(
    product_id: int,
    service: ProductServiceDep,
    restricted: AdminRestricted,
) -> ProductOut:
    return await service.get_product_by_id(product_id)


@router.post(
    "/create/product",
    response_model=ProductOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product: form_model(ProductIn),
    service: ProductServiceDep,
    restricted: AdminRestricted,
) -> ProductOut:

    return await service.create_product(product_in=product)


@router.put(
    "/update/{product_id}",
    response_model=ProductOut,
)
async def update_product(
    product_id: int,
    product: form_model(ProductIn),
    service: ProductServiceDep,
    restricted: AdminRestricted,
) -> ProductOut:
    return await service.update_product_by_id(product_id, product_in=product)


@router.delete(
    "/delete/{product_id}",
)
async def delete_product(
    service: ProductServiceDep,
    product_id: str,
    restricted: AdminRestricted,
) -> dict:
    await service.delete_product_by_id(delete_id=product_id)
    return {"successfully": True}

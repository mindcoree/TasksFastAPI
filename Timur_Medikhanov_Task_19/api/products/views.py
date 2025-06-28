from fastapi import APIRouter, status, Depends

from api.members.admins.dependencies import AdminRestricted
from core.config import settings
from type.annotated import form_model, query_model
from .dependencies import ProductServiceDep
from .schemas import ProductOut, ProductIn, ProductUpdatePartial, ProductUpdate
from ..common.pagination import PaginationProduct

router = APIRouter(prefix=settings.api.products.prefix, tags=["Products"])


@router.get(
    "/product/{product_id}",
    response_model=ProductOut,
    summary="Get a single product by ID",
    description="Retrieves a single product from the database based on its ID.",
    responses={
        200: {"description": "Successful Response", "model": ProductOut},
        404: {"description": "Product not found"},
    },
)
async def get_product(
    restricted: AdminRestricted,
    product_id: int,
    service: ProductServiceDep,
) -> ProductOut:
    return await service.get_product_by_id(product_id)


@router.get(
    "/list-products",
    summary="Get a list of products",
    description="Retrieves a list of products with pagination.",
    responses={
        200: {"description": "Successful Response", "model": list[ProductOut]},
    },
)
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
    summary="Create a new product",
    description="Creates a new product in the database.",
    responses={
        201: {"description": "Successful Response", "model": ProductOut},
        422: {"description": "Validation Error"},
    },
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
    summary="Update a product",
    description="Updates a product in the database.",
    responses={
        200: {"description": "Successful Response", "model": ProductOut},
        404: {"description": "Product not found"},
        422: {"description": "Validation Error"},
    },
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
    summary="Partially update a product",
    description="Partially updates a product in the database.",
    responses={
        200: {"description": "Successful Response", "model": ProductOut},
        404: {"description": "Product not found"},
        422: {"description": "Validation Error"},
    },
)
async def partial_update_product(
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
    summary="Delete a product",
    description="Deletes a product from the database.",
    responses={
        200: {"description": "Successful Response"},
        404: {"description": "Product not found"},
    },
)
async def delete_product(
    product_id: int,
    restricted: AdminRestricted,
    service: ProductServiceDep,
) -> dict:
    await service.delete_product_by_id(delete_id=product_id)
    return {"successfully": True}

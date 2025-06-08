from typing import Annotated

from fastapi import Depends

from api.common.dependencies import get_service
from core.db_helper import SessionDep
from .repository import ProductRepository
from .schemas import ProductOut
from .services import ProductService


async def get_product_service(session: SessionDep) -> ProductService:
    return await get_service(
        session=session,
        repository=ProductRepository,
        service_cls=ProductService,
    )


ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]


async def get_product_or_404(
    product_id: int,
    service: ProductServiceDep,
) -> ProductOut:
    return await service.ensure_instance_exists_by_id(id_instance=product_id)


ExistingProduct = Annotated[ProductOut, Depends(get_product_or_404)]

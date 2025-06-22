from typing import Annotated

from fastapi import Depends

from api.common.dependencies import get_service
from core.db_helper import SessionDep
from .repository import ProductRepository
from .schemas import ProductOut
from .services import ProductService
from core.redis import get_redis


async def get_product_service(
    session: SessionDep,
    redis_client=Depends(get_redis),
) -> ProductService:
    repo = ProductRepository(session=session)
    return ProductService(repository=repo, redis_client=redis_client)


ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]

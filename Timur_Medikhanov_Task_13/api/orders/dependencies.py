from core.db_helper import SessionDep
from .services import OrderService
from typing import Annotated
from fastapi import Depends


async def get_service(session: SessionDep) -> OrderService:
    return OrderService(session)


OrderServiceDep = Annotated[OrderService, Depends(get_service)]

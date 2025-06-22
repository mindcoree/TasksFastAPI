from fastapi import APIRouter

from core.config import settings
from .schemas import OrderCreate
from type.annotated import form_model
from api.members.users.dependencies import UserRestricted
from .dependencies import OrderServiceDep

router = APIRouter(prefix=settings.api.orders.prefix, tags=["ORDERS"])


@router.post("/create")
async def create_order(
    order_data: form_model(OrderCreate),
    restrict: UserRestricted,
    service: OrderServiceDep,
):
    user_id = int(restrict.sub)
    return await service.create_order_with_products(order_data, user_id)

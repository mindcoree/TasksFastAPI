from fastapi import APIRouter, status

from core.config import settings
from .schemas import OrderCreate, OrderOut
from type.annotated import form_model
from api.members.users.dependencies import UserRestricted
from .dependencies import OrderServiceDep

router = APIRouter(prefix=settings.api.orders.prefix, tags=["Orders"])


@router.post(
    "/create",
    response_model=OrderOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new order",
    description="Creates a new order with a list of products.",
    responses={
        201: {"description": "Successful Response", "model": OrderOut},
        422: {"description": "Validation Error"},
    },
)
async def create_order(
    order_data: form_model(OrderCreate),
    restrict: UserRestricted,
    service: OrderServiceDep,
) -> OrderOut:
    user_id = int(restrict.sub)
    return await service.create_order_with_products(order_data, user_id)

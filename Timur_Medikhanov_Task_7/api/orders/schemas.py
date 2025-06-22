from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, conint

from ..common.enums import OrderStatus, PaymentStatus
from ..common.order_product_association import OrderProductAssociation


class OrderProductCreate(BaseModel):
    product_id: int
    quantity: conint(gt=0)


class OrderCreate(BaseModel):
    products: list[OrderProductCreate]
    shipping_address: Optional[str] = None


class OrderOut(BaseModel):
    id: int
    member_id: int
    total_amount: Decimal
    status: OrderStatus
    payment_status: PaymentStatus
    shipping_address: Optional[str]
    products_association: List[OrderProductAssociation]
    created_at: datetime
    updated_at: datetime

    model_config = {"arbitrary_types_allowed": True}

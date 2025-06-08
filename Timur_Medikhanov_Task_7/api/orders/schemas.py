from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel

from ..common.enums import OrderStatus, PaymentStatus
from ..common.order_product_association import OrderProductAssociation


class OrderCreate(BaseModel):
    member_id: int
    products: List[OrderProductAssociation]
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

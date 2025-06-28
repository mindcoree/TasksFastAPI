from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, conint, Field

from ..common.enums import OrderStatus, PaymentStatus
from api.common.schemas_association import OrderProductAssociationSchema

class OrderProductCreate(BaseModel):
    product_id: int = Field(..., description="The unique identifier of the product.", example=1)
    quantity: conint(gt=0) = Field(..., description="The quantity of the product.", example=2)


class OrderCreate(BaseModel):
    products: list[OrderProductCreate]
    shipping_address: Optional[str] = Field(None, description="The shipping address for the order.", example="123 Main St, Anytown, USA")

    class Config:
        json_schema_extra = {
            "example": {
                "products": [
                    {"product_id": 1, "quantity": 2},
                    {"product_id": 2, "quantity": 1},
                ],
                "shipping_address": "123 Main St, Anytown, USA",
            }
        }


class OrderOut(BaseModel):
    id: int = Field(..., description="The unique identifier of the order.", example=1)
    member_id: int = Field(..., description="The unique identifier of the member who placed the order.", example=1)
    total_amount: Decimal = Field(..., description="The total amount of the order.", example=150.75)
    status: OrderStatus = Field(..., description="The current status of the order.", example=OrderStatus.PENDING)
    payment_status: PaymentStatus = Field(..., description="The payment status of the order.", example=PaymentStatus.PENDING)
    shipping_address: Optional[str] = Field(None, description="The shipping address for the order.", example="123 Main St, Anytown, USA")
    products_association: List[OrderProductAssociationSchema]
    created_at: datetime = Field(..., description="The timestamp when the order was created.")
    updated_at: datetime = Field(..., description="The timestamp when the order was last updated.")

    model_config = {"arbitrary_types_allowed": True}

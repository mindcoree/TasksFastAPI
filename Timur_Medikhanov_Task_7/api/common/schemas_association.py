from decimal import Decimal

from pydantic import BaseModel


class OrderProductAssociationSchema(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    discount: Decimal = 0.0

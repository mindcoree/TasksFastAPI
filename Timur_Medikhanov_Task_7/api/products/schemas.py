from decimal import Decimal

from pydantic import BaseModel
from datetime import datetime


class ProductIn(BaseModel):
    name: str
    description: str | None = None
    price: Decimal


class ProductOut(ProductIn):
    id: int
    created_at: datetime
    updated_at: datetime


class ProductUpdate(ProductIn):
    pass

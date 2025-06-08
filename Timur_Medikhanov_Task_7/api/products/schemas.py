from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class ProductIn(BaseModel):
    name: str
    description: str | None = None
    price: Decimal
    stock: Optional[int] = 0


class ProductOut(ProductIn):
    id: int
    created_at: datetime
    updated_at: datetime


class ProductUpdate(ProductIn):
    pass


class ProductUpdatePartial(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    stock: Optional[int] = None

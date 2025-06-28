from datetime import datetime
from typing import Optional

from pydantic import BaseModel, condecimal


class ProductIn(BaseModel):
    name: str
    description: str | None = None
    price: condecimal(gt=0)
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
    price: condecimal(gt=0) = None
    stock: Optional[int] = None

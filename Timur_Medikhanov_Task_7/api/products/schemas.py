from pydantic import BaseModel


class ProductIn(BaseModel):
    name: str
    description: str | None = None
    price: str


class ProductOut(ProductIn):
    id: int
    created_at: str
    updated_at: str


class ProductUpdate(ProductOut):
    pass

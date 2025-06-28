from datetime import datetime
from typing import Optional

from pydantic import BaseModel, condecimal, Field


class ProductIn(BaseModel):
    name: str = Field(..., description="Name of the product", example="Laptop")
    description: str | None = Field(None, description="Description of the product", example="A powerful laptop")
    price: condecimal(gt=0) = Field(..., description="Price of the product", example=1200.50)
    stock: Optional[int] = Field(0, description="Stock quantity of the product", example=100)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Laptop",
                "description": "A powerful laptop",
                "price": 1200.50,
                "stock": 100,
            }
        }


class ProductOut(ProductIn):
    id: int = Field(..., description="The unique identifier of the product.", example=1)
    created_at: datetime = Field(..., description="The timestamp when the product was created.")
    updated_at: datetime = Field(..., description="The timestamp when the product was last updated.")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Laptop",
                "description": "A powerful laptop",
                "price": 1200.50,
                "stock": 100,
                "created_at": "2025-06-29T12:00:00Z",
                "updated_at": "2025-06-29T12:00:00Z",
            }
        }


class ProductUpdate(ProductIn):
    pass


class ProductUpdatePartial(BaseModel):
    name: Optional[str] = Field(None, description="Name of the product", example="Gaming Laptop")
    description: Optional[str] = Field(None, description="Description of the product", example="An even more powerful gaming laptop")
    price: Optional[condecimal(gt=0)] = Field(None, description="Price of the product", example=1500.75)
    stock: Optional[int] = Field(None, description="Stock quantity of the product", example=50)

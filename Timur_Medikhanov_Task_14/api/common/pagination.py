from pydantic import BaseModel, Field


class Pagination(BaseModel):
    limit: int = Field(..., gt=0)
    offset: int = Field(..., ge=0)


class PaginationProduct(Pagination):
    pass

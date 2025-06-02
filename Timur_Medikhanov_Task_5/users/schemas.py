from typing import Annotated, Optional
from pydantic import BaseModel, Field
from .models import Role


class UserCreate(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=40)]
    password: Annotated[str, Field(min_length=8, max_length=40)]


class UserLogin(UserCreate):
    pass


class ResponseUser(BaseModel):
    id: int
    username: str


class UserSchemas(BaseModel):
    id: int | str
    username: str
    role: Optional[Role] = None


class TokenInfo(BaseModel):
    access: str
    refresh: str | None = None
    token_type: str


class UserPayload(BaseModel):
    sub: str
    username: str
    role: Optional[Role] = None

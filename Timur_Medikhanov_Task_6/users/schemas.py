from typing import Annotated, Optional

from pydantic import BaseModel, Field
from .models import Role


class UserCreate(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=40)]
    password: Annotated[str, Field(min_length=8, max_length=40)]


class UserLogin(UserCreate):
    pass


class AdminCreate(UserCreate):
    pass


class UserScheme(BaseModel):
    id: int
    username: str
    role: Role


class AdminScheme(UserScheme):
    pass


class ResponseUser(BaseModel):
    id: int
    username: str


class TokenInfo(BaseModel):
    access: str
    refresh: str
    token_type: str = "Cookie"


class UserPayload(BaseModel):
    sub: str
    username: str
    role: Optional[Role] = None

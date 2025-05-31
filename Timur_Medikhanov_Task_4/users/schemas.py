from typing import Annotated

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=40)]
    password: Annotated[str, Field(min_length=8, max_length=40)]


class UserLogin(UserCreate):
    pass


class ResponseUser(BaseModel):
    id: int
    username: str


class AccessToken(BaseModel):
    token: str
    token_type: str

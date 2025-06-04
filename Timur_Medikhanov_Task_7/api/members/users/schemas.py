from pydantic import BaseModel, EmailStr, Field
from typing import Annotated


from type.annotated import password, login
from api.common.enums import Role


class UserBase(BaseModel):
    login: login


class UserCredentials(UserBase):
    password: password


class UserCreate(UserCredentials):
    email: Annotated[
        EmailStr,
        Field(
            description="A valid email address.",
            examples=["user@example.com"],
        ),
    ]
    password: password


class TokenInfo(BaseModel):
    access: str
    refresh: str
    token_storage: str = "Cookie"


class UserInfo(UserBase):
    id: int
    role: Role

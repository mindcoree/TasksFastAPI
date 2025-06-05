from pydantic import BaseModel, EmailStr, Field
from typing import Annotated


from type.annotated import password, login
from api.common.enums import Role


class UserLogin(BaseModel):
    login: login


class UserCredentials(UserLogin):
    password: password


class UserCreate(UserCredentials):
    email: Annotated[
        EmailStr,
        Field(
            description="A valid email address.",
            examples=["user@example.com"],
        ),
    ]


class TokenInfo(BaseModel):
    access: str
    refresh: str
    token_storage: str = "Cookie"


class UserInfo(UserLogin):
    id: int
    role: Role

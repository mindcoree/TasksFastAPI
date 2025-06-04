from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
from type.annotated import password, login


class UserBase(BaseModel):
    id: int
    login: login


class AdminCreate(UserBase):
    password: password


class AdminInfo(AdminCreate):
    id: int

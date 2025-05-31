from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: str
    foo: int
    bar: int


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int


class UserScheme(BaseModel):
    username: str
    password: bytes
    email: EmailStr

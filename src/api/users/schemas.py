from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    foo: int
    bar: int


class UserCraete(UserBase):
    pass


class UserRead(UserBase):
    id: int

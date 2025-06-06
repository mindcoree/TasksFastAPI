from pydantic import BaseModel
from type.annotated import password, login


class AdminBase(BaseModel):
    login: login


class AdminCreate(AdminBase):
    password: password
    login: login
    email: str


class AdminInfo(AdminBase):
    id: int

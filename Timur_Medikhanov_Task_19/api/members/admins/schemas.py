from pydantic import BaseModel

from api.common.enums import Role
from type.annotated import password, login


class AdminBase(BaseModel):
    login: login


class AdminCreate(AdminBase):
    password: password
    login: login
    email: str


class AdminInfo(AdminBase):
    id: int
    role: Role

from pydantic import BaseModel
from type.annotated import password, login
from api.common.enums import Role


class AdminBase(BaseModel):
    login: login


class AdminCreate(AdminBase):
    password: password
    login: login
    email: str


class AdminInfo(AdminBase):
    id: int
    role: Role

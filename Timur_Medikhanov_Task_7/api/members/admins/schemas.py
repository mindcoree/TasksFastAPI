from pydantic import BaseModel
from type.annotated import password, login


class AdminBase(BaseModel):
    id: int
    login: login


class AdminCreate(AdminBase):
    password: password


class AdminInfo(AdminBase):
    pass

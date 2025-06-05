from api.common.base import Base
from type.annotated import ID_PK
from sqlalchemy.orm import Mapped
from api.common.mixins import BaseAccountMixin


class Admin(BaseAccountMixin, Base):
    __tablename__ = "admins"

    id: Mapped[ID_PK]

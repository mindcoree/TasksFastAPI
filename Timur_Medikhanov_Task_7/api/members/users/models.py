from api.common.base import Base
from api.common.mixins import BaseAccountMixin
from sqlalchemy.orm import Mapped, mapped_column
from type.annotated import ID_PK


class User(BaseAccountMixin, Base):
    __tablename__ = "users"

    id: Mapped[ID_PK]
    email: Mapped[str] = mapped_column(nullable=False, unique=True)

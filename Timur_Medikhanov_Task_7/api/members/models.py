from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.common.base import Base
from api.common.mixins import BaseAccountMixin
from type.annotated import ID_PK

if TYPE_CHECKING:
    from api.orders.models import Order


class Member(BaseAccountMixin, Base):
    __tablename__ = "members"

    id: Mapped[ID_PK]
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    orders: Mapped[list["Order"]] = relationship(back_populates="member")

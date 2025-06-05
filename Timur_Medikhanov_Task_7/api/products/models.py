from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import CheckConstraint

from api.common.base import Base
from api.common.mixins import TimestampMix
from type.annotated import ID_PK


class Product(TimestampMix, Base):
    __tablename__ = "products"
    __table_args__ = (CheckConstraint("price > 0", name="price_positive"),)

    id: Mapped[ID_PK]
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    price: Mapped[int]

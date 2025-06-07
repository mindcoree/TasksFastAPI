from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint, DECIMAL
from typing import TYPE_CHECKING
from api.common.base import Base
from api.common.mixins import TimestampMix
from type.annotated import ID_PK

if TYPE_CHECKING:
    from ..common.order_product_association import OrderProductAssociation


class Product(TimestampMix, Base):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("price > 0", name="price_positive"),
        CheckConstraint("stock >= 0", name="stock_non_negative"),
    )

    id: Mapped[ID_PK]
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    stock: Mapped[int] = mapped_column(default=0)

    orders_association: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="product"
    )

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, PrimaryKeyConstraint, CheckConstraint, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.common.base import Base

if TYPE_CHECKING:
    from api.orders.models import Order
    from api.products.models import Product


class OrderProductAssociation(Base):
    __tablename__ = "order_product_association"
    __table_args__ = (
        PrimaryKeyConstraint("order_id", "product_id", name="pk_order_product"),
        CheckConstraint("quantity > 0", name="quantity_positive"),
        CheckConstraint("discount >= 0", name="discount_non_negative"),
        CheckConstraint("unit_price > 0", name="unit_price_positive"),
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), primary_key=True
    )
    quantity: Mapped[int] = mapped_column(default=1)
    unit_price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    discount: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=10, scale=2), default=0.0
    )

    order: Mapped["Order"] = relationship(back_populates="products_association")
    product: Mapped["Product"] = relationship(back_populates="orders_association")

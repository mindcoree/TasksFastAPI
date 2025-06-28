from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DECIMAL, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from type.annotated import ID_PK
from core.base import Base
from ..common.enums import OrderStatus, PaymentStatus
from ..common.mixins import MemberRelationMix
from ..common.mixins import TimestampMix

if TYPE_CHECKING:
    from api.common.order_product_association import OrderProductAssociation


class Order(MemberRelationMix, TimestampMix, Base):
    __tablename__ = "orders"
    __member_back_populates = "orders"
    __table_args__ = (
        CheckConstraint("total_amount >= 0", name="total_amount_non_negative"),
    )
    id: Mapped[ID_PK]
    shipping_address: Mapped[str] = mapped_column(nullable=True)
    order_status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, name="order_status", Enumdefault=OrderStatus.PENDING)
    )
    total_amount: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=10, scale=2), default=0.0
    )
    payment_status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus, name="payment_status", default=PaymentStatus.PENDING)
    )

    products_association: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="order"
    )

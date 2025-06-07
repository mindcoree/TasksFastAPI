from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, CheckConstraint, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..common.enums import OrderStatus, PaymentStatus
from ..common.base import Base
from type.annotated import ID_PK
from ..common.mixins import TimestampMix

if TYPE_CHECKING:
    from api.members.models import Member
    from api.common.order_product_association import OrderProductAssociation


class Order(TimestampMix, Base):
    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint("total_amount >= 0", name="total_amount_non_negative"),
    )
    id: Mapped[ID_PK]
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id", ondelete="CASCADE"))
    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.PENDING)
    total_amount: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=10, scale=2), default=0.0
    )
    shipping_address: Mapped[str] = mapped_column(nullable=True)
    payment_status: Mapped[PaymentStatus] = mapped_column(default=PaymentStatus.PENDING)

    member: Mapped["Member"] = relationship(back_populates="orders")
    products_association: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="order"
    )

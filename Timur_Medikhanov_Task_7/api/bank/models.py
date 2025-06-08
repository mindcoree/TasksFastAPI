from typing import TYPE_CHECKING

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from api.common.base import Base
from api.common.enums import BankName, PaymentSystem, AccountStatus
from api.common.mixins import TimestampMix, MemberRelationMix
from type.annotated import ID_PK

if TYPE_CHECKING:
    pass


class BankAccount(MemberRelationMix, TimestampMix, Base):
    __tablename__ = "bank_accounts"
    __member_back_populates = "bank_accounts"
    id: Mapped[ID_PK]
    bank_name: Mapped[BankName] = mapped_column(Enum(BankName, name="bank_name"))
    encrypted_account_number: Mapped[str] = mapped_column(
        nullable=False, comment="Зашифрованный номер карты"
    )
    hash_account_number: Mapped[str] = mapped_column(
        nullable=False, comment="Хешированный номер карты"
    )
    masked_account_number: Mapped[str] = mapped_column(
        nullable=False, comment="Маскированный номер (**** **** **** 1234)"
    )
    is_default: Mapped[bool] = mapped_column(default=False)
    payment_system: Mapped[PaymentSystem] = mapped_column(
        Enum(PaymentSystem, name="payment_system")
    )
    account_status: Mapped[AccountStatus] = mapped_column(
        Enum(AccountStatus, name="account_status")
    )

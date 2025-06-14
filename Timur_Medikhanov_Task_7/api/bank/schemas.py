from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field
from ..common.enums import BankName, PaymentSystem, AccountStatus


class BaseAccount(BaseModel):
    bank_name: BankName
    payment_system: PaymentSystem
    balance: Decimal
    is_default: bool = Field(description="Указатель основной карты")


class BankAccountCreate(BaseAccount):
    member_id: int
    masked_account_number: str
    encrypted_account_number: str
    hash_account_number: str
    account_status: AccountStatus


class AccountIn(BaseAccount):
    account_number: str


class AccountOut(BaseAccount):
    id: int
    masked_account_number: str
    account_status: AccountStatus
    created_at: datetime
    updated_at: datetime


class AccountFilter(BaseModel):
    bank_name: BankName
    payment_system: PaymentSystem


class AccountFilterData(AccountFilter):
    member_id: int


class AccountUpdateBalance(BaseModel):
    bank_name: BankName
    payment_system: PaymentSystem
    account_number: str
    balance: Decimal

from datetime import datetime

from pydantic import BaseModel
from ..common.enums import BankName, PaymentSystem, AccountStatus


class BaseAccount(BaseModel):
    bank_name: BankName
    payment_system: PaymentSystem
    is_default: bool


class AccountIn(BaseAccount):
    account_number: str


class AccountOut(BaseAccount):
    id: int
    masked_account_number: str
    account_status: AccountStatus
    created_at: datetime
    updated_at: datetime

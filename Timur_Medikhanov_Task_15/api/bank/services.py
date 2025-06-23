from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from .repository import BankAccountRepository
from .models import BankAccount
from utils import fernet
from sqlalchemy.exc import IntegrityError
from .schemas import (
    AccountIn,
    BankAccountCreate,
    AccountFilterData,
    AccountFilter,
    AccountUpdateBalance,
)

from ..common.enums import AccountStatus
from .exceptions import (
    InvalidBankAccountData,
    BankAccountAlreadyExists,
    BankAccountNotFound,
)
from ..common.services import BaseService


class BankAccountService(BaseService[BankAccount]):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = BankAccountRepository(self.session)
        super().__init__(repository=self.repo, model=BankAccount)

    @staticmethod
    def validate_card_number(card_number, balance) -> None:
        if not (card_number.isdigit() and len(card_number) == 16):
            raise InvalidBankAccountData("The wrong format of the card number")

        if balance < 0:
            raise InvalidBankAccountData("balance must be positive")

    async def create_account(
        self, account_info: AccountIn, member_id: int
    ) -> BankAccount:
        card_number = account_info.account_number
        self.validate_card_number(card_number, account_info.account_number)

        hash_account_number = await fernet.hash_card_number(card_number)
        encrypted = await fernet.encrypt_card_number(card_number)
        masked = await fernet.mask_card_number(card_number)

        account = BankAccountCreate(
            **account_info.model_dump(exclude={"account_number"}),
            member_id=member_id,
            masked_account_number=masked,
            hash_account_number=hash_account_number,
            encrypted_account_number=encrypted,
            account_status=AccountStatus.ACTIVE,
        )

        try:
            return await self.repo.create_bank_account(
                account_info=account,
                is_default=account.is_default,
            )
        except IntegrityError:
            raise BankAccountAlreadyExists(card_number=card_number)

    async def get_list_bank_accounts(
        self,
        account_id: int,
    ) -> Sequence[BankAccount]:
        return await self.repo.get_all_bank_accounts(account_id)

    async def get_list_bank_account_with_filters(
        self, filters_in: AccountFilter, member_id: int
    ) -> Sequence[BankAccount]:
        filters = AccountFilterData(**filters_in.model_dump(), member_id=member_id)
        return await self.repo.get_bank_account_with_filters(filters)

    async def top_up_balance_account(
        self, account_info: AccountUpdateBalance, member_id: int
    ) -> BankAccount:

        card_number = account_info.account_number
        self.validate_card_number(card_number, account_info.balance)
        hash_account_number = await fernet.hash_card_number(card_number)
        bank_account = await self.repo.top_up_balance_account(
            hash_account_number=hash_account_number,
            member_id=member_id,
            balance=account_info.balance,
        )
        if bank_account is None:
            raise BankAccountNotFound(card_number=card_number)

        return bank_account

from decimal import Decimal

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence
from .schemas import BankAccountCreate, AccountFilterData
from ..common.repository import BaseRepository
from .models import BankAccount


class BankAccountRepository(BaseRepository[BankAccount]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=BankAccount)

    async def create_bank_account(
        self,
        account_info: BankAccountCreate,
        is_default: bool,
    ) -> BankAccount:
        if is_default:
            stmt = (
                update(BankAccount)
                .where(
                    BankAccount.member_id == account_info.member_id,
                    BankAccount.is_default == True,
                )
                .values(is_default=False)
            )
            await self.session.execute(stmt)
        return await self.create(account_info.model_dump())

    async def get_all_bank_accounts(
        self,
        account_id: int,
    ) -> Sequence[BankAccount]:
        stmt = (
            select(BankAccount)
            .where(BankAccount.member_id == account_id)
            .order_by(BankAccount.created_at)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_bank_account_with_filters(
        self, filters: AccountFilterData
    ) -> Sequence[BankAccount]:
        return await self.filter_by(filters.model_dump())

    async def top_up_balance_account(
        self, hash_account_number: str, member_id: int, balance: Decimal
    ) -> BankAccount | None:

        stmt = select(BankAccount).where(
            BankAccount.member_id == member_id,
            BankAccount.hash_account_number == hash_account_number,
        )

        result = await self.session.execute(stmt)
        bank_account = result.scalar_one_or_none()

        if bank_account is None:
            return None

        bank_account.balance += balance
        self.session.add(bank_account)
        await self.session.commit()
        await self.session.refresh(bank_account)
        return bank_account

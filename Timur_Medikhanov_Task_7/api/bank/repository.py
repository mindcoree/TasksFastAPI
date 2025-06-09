from typing import Any, Sequence

from sqlalchemy import select, Result, update, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession


from ..common.repository import BaseRepository
from .models import BankAccount


class BankAccountRepository(BaseRepository[BankAccount]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=BankAccount)

    async def card_exists_by_hash(self, account_id: int, hash_value: str) -> Sequence[Row[Any] | RowMapping | Any]:
        stmt = select(BankAccount.hash_account_number).where(
            BankAccount.hash_account_number == hash_value,
            BankAccount.member_id == account_id,
        )
        result: Result = await self.session.execute(stmt)
        return result.scalars().all()

    async def unset_default_cards_for_member(self, account_id: int):
        stmt = (
            update(BankAccount)
            .where(
                BankAccount.member_id == account_id,
                BankAccount.is_default == True,
            )
            .values(is_default=False)
        )
        await self.session.execute(stmt)
        await self.session.commit()

from sqlalchemy import select, Result, and_, update
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import BankAccountCreate
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
        account = BankAccount(**account_info.model_dump())
        self.session.add(account)
        await self.session.commit()

from typing import Annotated

from .services import BankAccountService
from fastapi import Depends
from core.db_helper import SessionDep


async def get_bank_account_service(session: SessionDep) -> BankAccountService:
    return BankAccountService(session)


BankAccountServiceDep = Annotated[BankAccountService, Depends(get_bank_account_service)]

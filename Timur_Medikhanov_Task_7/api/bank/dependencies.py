from typing import Annotated

from .repository import BankAccountRepository
from .services import BankAccountService
from ..common.dependencies import get_service
from fastapi import Depends
from core.db_helper import SessionDep


async def get_bank_account_service(session: SessionDep) -> BankAccountService:
    return await get_service(
        session=session,
        repository=BankAccountRepository,
        service_cls=BankAccountService,
    )


BankAccountServiceDep = Annotated[BankAccountService, Depends(get_bank_account_service)]

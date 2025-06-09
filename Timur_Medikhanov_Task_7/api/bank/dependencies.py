from fastapi import Depends
from typing import Annotated
from core.db_helper import SessionDep
from api.common.dependencies import get_service
from .repository import BankAccountRepository
from .services import BankAccountServices
async def get_bank_account_service(session:SessionDep) -> BankAccountServices:
    return await  get_service(
        session=session,
        repository=BankAccountRepository,
        service_cls=BankAccountServices,
    )


BankAccountServicesDep = Annotated[BankAccountServices,Depends(get_bank_account_service)]
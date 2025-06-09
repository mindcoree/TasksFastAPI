from fastapi import APIRouter
from core.config import settings
from .dependencies import BankAccountServicesDep
from api.members.users.dependencies import UserRestricted
from .schemas import AccountOut ,AccountIn
from type.annotated import form_model
router = APIRouter(prefix=settings.api.bk.prefix, tags=["BANK-ACCOUNT"])


async def create_account_bank(
        restricted: UserRestricted,
        service:BankAccountServicesDep,
        account_in: form_model(AccountIn),
) -> AccountOut:
    return await service.create_account(account_info=account_in)

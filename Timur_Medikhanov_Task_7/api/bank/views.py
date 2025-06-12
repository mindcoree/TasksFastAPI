from fastapi import APIRouter
from core.config import settings
from .schemas import AccountIn, AccountOut
from .dependencies import BankAccountServiceDep
from type.annotated import form_model
from api.members.users.dependencies import UserRestricted

router = APIRouter(prefix=settings.api.bk.prefix, tags=["BANK-ACCOUNT"])


@router.post("/create")
async def create_account_bank(
    account: form_model(AccountIn),
    service: BankAccountServiceDep,
    restrict: UserRestricted,
) -> AccountOut:
    return await service.create_account(
        account_info=account,
        member_id=int(restrict.sub),
    )

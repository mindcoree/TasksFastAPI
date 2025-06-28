from typing import Sequence

from fastapi import APIRouter
from starlette import status

from core.config import settings
from .schemas import AccountIn, AccountOut, AccountFilter, AccountUpdateBalance
from .dependencies import BankAccountServiceDep
from api.members.users.dependencies import UserRestricted
from type.annotated import query_model, form_model

router = APIRouter(prefix=settings.api.bk.prefix, tags=["BANK-ACCOUNT"])


@router.post(
    "/create",
    response_model=AccountOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_account_bank(
    account: form_model(AccountIn),
    service: BankAccountServiceDep,
    restrict: UserRestricted,
) -> AccountOut:
    return await service.create_account(
        account_info=account,
        member_id=int(restrict.sub),
    )


@router.get("/list", response_model=Sequence[AccountOut])
async def get_list_account(
    restrict: UserRestricted,
    service: BankAccountServiceDep,
) -> Sequence[AccountOut]:
    id_member = int(restrict.sub)
    return await service.get_list_bank_accounts(id_member)


@router.get("/list-filters", response_model=Sequence[AccountOut])
async def get_list_account_with_filter(
    restrict: UserRestricted,
    filters: query_model(AccountFilter),
    service: BankAccountServiceDep,
) -> Sequence[AccountOut]:
    member_id = int(restrict.sub)
    return await service.get_list_bank_account_with_filters(
        filters_in=filters, member_id=member_id
    )


@router.patch("/balance/top-up", response_model=AccountOut)
async def top_up_balance_account(
    restrict: UserRestricted,
    service: BankAccountServiceDep,
    account_info: form_model(AccountUpdateBalance),
) -> AccountOut:
    member_id = int(restrict.sub)
    bank_account = await service.top_up_balance_account(
        account_info=account_info, member_id=member_id
    )
    return bank_account

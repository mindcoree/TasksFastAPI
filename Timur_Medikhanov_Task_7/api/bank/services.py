from .repository import BankAccountRepository
from .models import BankAccount
from fastapi import HTTPException, status
from utils import fernet
from .schemas import AccountIn
from ..common.enums import AccountStatus


class BankAccountServices:
    repo: BankAccountRepository

    async def create_account(self, account_info: AccountIn, member_id) -> BankAccount:
        card_number = account_info.account_number

        if not (card_number.isdigit() and len(card_number) == 16):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The wrong format of the card number",
            )

        hash_account_number = await fernet.hash_card_number(card_number)

        is_duplicate = await self.repo.card_exists_by_hash(
            account_id=member_id,
            hash_value=hash_account_number,
        )
        if is_duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Such an account already exists.",
            )

        encrypted = await fernet.encrypt_card_number(account_info.account_number)
        masked = fernet.mask_card_number(account_info.account_number)

        account = account_info.model_dump(exclude={"account_number"})
        account.update(
            {
                "member_id": member_id,
                "masked_account_number": masked,
                "encrypted_account_number": encrypted,
                "hash_account_number": hash_account_number,
                "account_status": AccountStatus.ACTIVE,
            },
        )

        if account_info.is_default:
            await self.repo.unset_default_cards_for_member(member_id)

        return await self.repo.create(account)

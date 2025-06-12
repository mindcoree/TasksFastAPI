from .repository import BankAccountRepository
from .models import BankAccount
from utils import fernet
from sqlalchemy.exc import IntegrityError
from .schemas import AccountIn, BankAccountCreate
from ..common.enums import AccountStatus
from .exceptions import InvalidBankAccountData, BankAccountAlreadyExists


class BankAccountService:
    repo: BankAccountRepository

    async def create_account(
        self, account_info: AccountIn, member_id: int
    ) -> BankAccount:
        card_number = account_info.account_number

        if not (card_number.isdigit() and len(card_number) == 16):
            raise InvalidBankAccountData("The wrong format of the card number")

        if account_info.balance < 0:
            raise InvalidBankAccountData("balance must be positive")

        hash_account_number = await fernet.hash_card_number(card_number)
        encrypted = await fernet.encrypt_card_number(card_number)
        masked = fernet.mask_card_number(card_number)

        account = BankAccountCreate(
            **account_info.model_dump(exclude={"account_number"}),
            member_id=member_id,
            masked_account_number=masked,
            hash_account_number=hash_account_number,
            encrypted_account_number=encrypted,
            account_status=AccountStatus.ACTIVE,
        )

        try:
            return await self.repo.create_bank_account(
                account_info=account,
                is_default=account.is_default,
            )
        except IntegrityError:
            raise BankAccountAlreadyExists(card_number=card_number)

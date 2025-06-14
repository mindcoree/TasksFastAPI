from core.exceptions import AppException


class InvalidBankAccountData(AppException.InvalidData):
    def __init__(self, reason: str):
        super().__init__(reason=reason)


class BankAccountAlreadyExists(AppException.AlreadyExists):
    def __init__(self, card_number):
        super().__init__(field=f"card_number: {card_number}", model="BankAccount")


class BankAccountNotFound(AppException.NotFoundId):
    def __init__(self, card_number):
        super().__init__(
            field_name="card number", value=card_number, model="BankAccount"
        )

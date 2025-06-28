from core.exceptions import AppException


class OrderInvalidData(AppException.InvalidData):
    def __init__(self, reason: str):
        super().__init__(reason)

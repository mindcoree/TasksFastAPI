from core.exceptions import AppException


class ProductNotFoundId(AppException.NotFoundId):
    def __init__(self, product_id: int):
        super().__init__(id_=product_id, model="Product")


class ProductAlreadyExists(AppException.AlreadyExists):
    def __init__(self, name: str):
        super().__init__(field=f"name: {name}", model="Product")


class AlreadyExistsError(Exception):
    def __init__(self, message: str = "Resource already exists"):
        self.message = message
        super().__init__(self.message)


class InvalidProductData(AppException.InvalidData):
    def __init__(self, reason: str = "Invalid product data"):
        super().__init__(reason)

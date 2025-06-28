from typing import Any

from fastapi import HTTPException, status


class AppException(HTTPException):
    """Базовое исключение приложения."""

    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

    class NotFoundId(HTTPException):
        def __init__(self, field_name: str, value: Any, model: str):
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{model} with {field_name} = {value} not found",
            )

    class AlreadyExists(HTTPException):
        def __init__(self, field: str, model: str):
            super().__init__(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{model} with field='{field}' already exists",
            )

    class InvalidData(HTTPException):
        def __init__(self, reason: str):
            super().__init__(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=reason,
            )

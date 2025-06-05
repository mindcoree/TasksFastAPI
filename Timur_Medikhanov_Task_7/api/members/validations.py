from type.jwt import TOKEN_TYPE_FIELD

from fastapi import HTTPException, status
from pydantic import BaseModel
from typing import TypeVar, Generic
from api.common.services import BaseAuthService

T = TypeVar("T", bound=BaseModel)


async def validations_token_type(token_type: str, payload: dict):
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type != token_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    return True


class AuthValidator(Generic[T]):
    def __init__(self, service: BaseAuthService[T]):
        self.service: BaseAuthService[T] = service

    async def verify_login(self, login: str) -> T | None:
        await self.service.verification_login(login)

    async def verify_email(self, email: str) -> T | None:
        await self.service.verification_email(email)

    async def validate_create(self, data: T) -> T | None:
        await self.verify_login(data.login)
        await self.verify_email(data.email)

    async def verify_credentials(self, credentials: T) -> T:
        return await self.service.verify_credentials(credentials=credentials)

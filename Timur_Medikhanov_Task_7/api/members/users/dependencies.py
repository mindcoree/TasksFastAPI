from fastapi import Depends, HTTPException, status

from .models import User
from .repository import UserAuthRepository
from .services import UserAuthService
from api.common.dependencies import get_service, make_access_token_dependency
from typing import Annotated
from core.db_helper import SessionDep
from ..validations import AuthValidator


async def get_user_auth_service(session: SessionDep) -> UserAuthService:
    return await get_service(
        session=session,
        repository=UserAuthRepository,
        service_cls=UserAuthService,
    )


UserAuthServiceDep = Annotated[UserAuthService, Depends(get_user_auth_service)]


async def get_user_auth_validator(service: UserAuthServiceDep) -> AuthValidator[User]:
    return AuthValidator(service=service)


UserAuthValidatorDep = Annotated[AuthValidator[User], Depends(get_user_auth_validator)]


_get_user_access_token_payload = make_access_token_dependency(get_user_auth_service)
AccessTokenPayloadUser = Annotated[dict, Depends(_get_user_access_token_payload)]


async def restrict_to_user(payload: AccessTokenPayloadUser) -> dict:
    role = payload.get("role")
    if role != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="forbidden User"
        )

    return payload


UserRestricted = Annotated[dict, Depends(restrict_to_user)]

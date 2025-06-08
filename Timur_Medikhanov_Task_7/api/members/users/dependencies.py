from typing import Annotated

from fastapi import Depends, HTTPException, status

from api.common.dependencies import get_service, make_access_token_dependency
from api.members.models import Member
from core.db_helper import SessionDep
from utils.auth import AccessTokenPayload
from .repository import UserAuthRepository
from .services import UserAuthService
from ..validations import AuthValidator


async def get_user_auth_service(session: SessionDep) -> UserAuthService:
    return await get_service(
        session=session,
        repository=UserAuthRepository,
        service_cls=UserAuthService,
    )


UserAuthServiceDep = Annotated[UserAuthService, Depends(get_user_auth_service)]


async def get_user_auth_validator(
    service: UserAuthServiceDep,
) -> AuthValidator[Member]:
    return AuthValidator(service=service)


UserAuthValidatorDep = Annotated[
    AuthValidator[Member], Depends(get_user_auth_validator)
]


_get_user_access_token_payload = make_access_token_dependency(get_user_auth_service)
AccessTokenPayloadUser = Annotated[
    AccessTokenPayload, Depends(_get_user_access_token_payload)
]


async def restrict_to_user(payload: AccessTokenPayloadUser) -> AccessTokenPayload:
    role = payload.role
    if role != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="forbidden User"
        )

    return payload


UserRestricted = Annotated[AccessTokenPayload, Depends(restrict_to_user)]

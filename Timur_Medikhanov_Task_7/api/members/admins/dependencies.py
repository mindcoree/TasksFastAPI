from typing import Annotated

from fastapi import Depends, HTTPException, status

from api.common.dependencies import get_service, make_access_token_dependency
from core.db_helper import SessionDep
from utils.auth import AccessTokenPayload
from .repository import AdminAuthRepository
from .services import AdminAuthService


async def get_admin_auth_service(session: SessionDep) -> AdminAuthService:
    return await get_service(
        session=session,
        repository=AdminAuthRepository,
        service_cls=AdminAuthService,
    )


AdminAuthServiceDep = Annotated[AdminAuthService, Depends(get_admin_auth_service)]

# async def get_admin_payload(
#     request: Request,
#     response: Response,
#     service: AdminAuthServiceDep,
# ) -> :
#     return await service.access_token_payload(request,response)
#
#
# AccessTokenPayloadAdmin = Annotated[dict,Depends(get_admin_payload)]

# 4) Функция-зависимость для AdminAccessTokenPayload

_get_admin_access_token_payload = make_access_token_dependency(get_admin_auth_service)
AccessTokenPayloadAdmin = Annotated[
    AccessTokenPayload, Depends(_get_admin_access_token_payload)
]


async def restrict_to_admin(payload: AccessTokenPayloadAdmin) -> dict:
    if payload.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    return payload


AdminRestricted = Annotated[AccessTokenPayload, Depends(restrict_to_admin)]

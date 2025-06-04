from fastapi import Depends, HTTPException, status
from typing import Annotated
from core.db_helper import SessionDep
from .repository import AdminAuthRepository
from .services import AdminAuthService
from api.common.dependencies import get_service, make_access_token_dependency


async def get_admin_auth_service(session: SessionDep) -> AdminAuthService:
    return await get_service(
        session=session,
        repository=AdminAuthRepository,
        service_cls=AdminAuthService,
    )


AdminAuthServiceDep = Annotated[AdminAuthService, Depends(get_admin_auth_service)]


# 4) Функция-зависимость для AdminAccessTokenPayload
_get_admin_access_token_payload = make_access_token_dependency(get_admin_auth_service)
AccessTokenPayloadAdmin = Annotated[dict, Depends(_get_admin_access_token_payload)]


async def current_admin(payload: AccessTokenPayloadAdmin) -> dict:
    role = payload.get("role")
    if role != "admins":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="forbidden admins"
        )
    return payload


CurrentAdmin = Annotated[dict, Depends(current_admin)]

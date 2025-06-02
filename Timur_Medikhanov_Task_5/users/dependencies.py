from typing import Annotated
from fastapi import Depends, Form, Request, Response, HTTPException, status
from .schemas import UserCreate, UserLogin, UserSchemas, UserPayload
from .services import UserAuthService
from .repository import UserRepository
from core.db_helper import SessionDep
from utils import auth


async def get_user_auth_service(session: SessionDep) -> UserAuthService:
    repository = UserRepository(session=session)
    return UserAuthService(repository=repository)


UserAuthServiceDep = Annotated[UserAuthService, Depends(get_user_auth_service)]


async def check_unique_user(
    check_user: Annotated[UserCreate, Form()],
    user_auth_service: UserAuthServiceDep,
) -> UserCreate:
    return await user_auth_service.check_unique_user(check_user=check_user)


CheckUniqueUsers = Annotated[UserCreate, Depends(check_unique_user)]


async def verify_credentials(
    sign_in_user: Annotated[UserLogin, Form()],
    user_auth_service: UserAuthServiceDep,
) -> UserSchemas:
    return await user_auth_service.verify_credentials(sign_in_user=sign_in_user)


VerificationUser = Annotated[UserSchemas, Depends(verify_credentials)]


async def access_token_payload(
    request: Request,
    response: Response,
    user_auth_service: UserAuthServiceDep,
) -> dict:
    payload = getattr(request.state, "user_payload", None)
    if payload:
        return payload

    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh-token is not provided",
        )

    user = await user_auth_service.refresh_access_token_and_get_user(
        refresh_token=refresh_token, response=response
    )
    payload = auth.create_payload(payload_user=user)
    return payload


AccessTokenPyload = Annotated[dict, Depends(access_token_payload)]


async def get_current_user(payload: AccessTokenPyload) -> dict:
    role = payload.get("role")
    if role != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN User"
        )
    return payload


CurrentUser = Annotated[UserPayload, Depends(get_current_user)]
# CurrentUser = Annotated[dict, Depends(get_current_user)]


async def get_current_admin(payload: AccessTokenPyload) -> dict:
    role = payload.get("role")
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN admin "
        )
    return payload


CurrentAdmin = Annotated[UserPayload, Depends(get_current_admin)]

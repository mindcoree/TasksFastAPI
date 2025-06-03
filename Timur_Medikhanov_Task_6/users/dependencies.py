from typing import Annotated
from fastapi import Depends, Form, Request, Response, HTTPException, status
from .schemas import UserCreate, UserLogin, UserScheme
from .repository import RepositoryUser
from core.db_helper import SessionDep
from .services import UserAuthService
from utils import auth


async def get_user_auth_service(session: SessionDep) -> UserAuthService:
    repository = RepositoryUser(session=session)
    return UserAuthService(repository=repository)


UserAuthServiceDep = Annotated[UserAuthService, Depends(get_user_auth_service)]


async def check_unique_user(
    user_auth_service: UserAuthServiceDep,
    check_user: Annotated[UserCreate, Form()],
) -> UserCreate:
    return await user_auth_service.check_unique_user(check_user=check_user)


CheckUniqueUser = Annotated[UserCreate, Depends(check_unique_user)]


async def verify_credentials(
    user_auth_service: UserAuthServiceDep, credentials: Annotated[UserLogin, Form()]
) -> UserScheme:
    return await user_auth_service.verify_credentials(credentials=credentials)


VerifiedUser = Annotated[UserScheme, Depends(verify_credentials)]


async def access_token_payload(
    request: Request, response: Response, user_auth_service: UserAuthServiceDep
) -> UserScheme:
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
        response=response, refresh_token=refresh_token
    )

    payload = auth.create_payload(user_payload=user)
    return payload


AccessTokenPyload = Annotated[dict, Depends(access_token_payload)]


async def current_user(payload: AccessTokenPyload) -> dict:
    role = payload.get("role")
    if role != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="forbidden User"
        )

    return payload


CurrentUser = Annotated[dict, Depends(current_user)]


async def current_admin(payload: AccessTokenPyload) -> dict:
    role = payload.get("role")
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="forbidden admin"
        )
    return payload


CurrentAdmin = Annotated[dict, Depends(current_admin)]

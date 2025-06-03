from typing import Callable, Awaitable

from fastapi import Request, HTTPException, status, Response
from jwt.exceptions import InvalidTokenError

from main import main_app
from utils import auth
from validations import validations_token_type
from type.jwt import ACCESS_TOKEN_TYPE


@main_app.middleware("http")
async def verify_jwt_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
):
    public_paths = {"/login", "/register", "/refresh", "/docs", "/openapi.json"}
    if request.url.path in public_paths:
        return await call_next(request)

    token = request.cookies.get("access_token")
    request.state.user_payload = None

    if token:
        try:
            payload = await auth.decode_jwt(token=token)
            await validations_token_type(ACCESS_TOKEN_TYPE, payload)
            request.state.user_payload = payload
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
            )
    return await call_next(request)

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
        response = await call_next(request)
        return response

    access_token = request.cookies.get("access_token")
    try:
        if access_token:
            access_payload = await auth.decode_jwt(token=access_token)
            await validations_token_type(
                token_type=ACCESS_TOKEN_TYPE, payload=access_payload
            )
            request.state.user_payload = access_payload
        else:
            request.state.user_payload = None
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )

    response = await call_next(request)
    return response

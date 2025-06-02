import bcrypt
import jwt
from datetime import datetime, timezone, timedelta
from functools import lru_cache
from core.config import settings
from type.jwt import TOKEN_TYPE_FIELD, REFRESH_TOKEN_TYPE, ACCESS_TOKEN_TYPE
from users.schemas import ResponseUser, UserSchemas
from fastapi import Response


@lru_cache(maxsize=1)
def get_private_key() -> str:
    return settings.auth.private_key.read_text()


@lru_cache(maxsize=1)
def get_public_key() -> str:
    return settings.auth.public_key.read_text()


import asyncio


async def encode_jwt(
    payload: dict,
    private_key: str = get_private_key(),
    algorithm: str = settings.auth.algorithm,
    expire_minutes: int = settings.auth.access_token_expire_min,
    expire_timedelta: timedelta | None = None,
) -> str:
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    payload.update(
        exp=int(expire.timestamp()),
        iat=int(now.timestamp()),
    )
    return await asyncio.to_thread(
        jwt.encode,
        payload=payload,
        key=private_key,
        algorithm=algorithm,
    )


async def decode_jwt(
    token: str,
    public_key: str = get_public_key(),
    algorithm: str = settings.auth.algorithm,
) -> dict:
    return await asyncio.to_thread(
        jwt.decode, jwt=token, key=public_key, algorithms=[algorithm]
    )


async def hash_password(password: str) -> str:
    salt = await asyncio.to_thread(bcrypt.gensalt)
    password_bytes: bytes = password.encode()
    hashed_password: bytes = await asyncio.to_thread(
        bcrypt.hashpw, password_bytes, salt
    )
    return hashed_password.decode("utf-8")


async def verify_password(password: str, hashed_password: str) -> bool:
    return await asyncio.to_thread(
        bcrypt.checkpw,
        password=password.encode(),
        hashed_password=hashed_password.encode(),
    )


async def create_jwt(
    token_data: dict,
    token_type: str,
    expire_minutes: int = settings.auth.access_token_expire_min,
    expire_timedelta: timedelta | None = None,
) -> str:
    payload = {TOKEN_TYPE_FIELD: token_type}
    payload.update(token_data)
    return await encode_jwt(
        payload=payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


async def create_access_token(user_info: UserSchemas) -> str:
    payload = create_payload(payload_user=user_info)
    return await create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=payload,
        expire_minutes=settings.auth.access_token_expire_min,
    )


async def create_refresh_token(user_info: UserSchemas) -> str:
    payload = {
        "sub": str(user_info.id),
    }
    return await create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=payload,
        expire_timedelta=timedelta(days=settings.auth.refresh_token_expire_days),
    )


def create_payload(payload_user: UserSchemas) -> dict:
    payload = {
        "sub": str(payload_user.id),
        "username": payload_user.username,
        "role": payload_user.role,
    }
    return payload


async def set_token_cookie(
    response: Response,
    key: str,
    value: str,
    max_age: int,
    httponly: bool = True,
    samesite: str = "lax",
    secure: bool = False,
) -> None:
    response.set_cookie(
        key=key,
        value=value,
        httponly=httponly,
        samesite=samesite,
        secure=secure,
        max_age=max_age,
    )

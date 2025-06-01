import bcrypt
import jwt
from datetime import datetime, timezone, timedelta
from functools import lru_cache
from core.config import settings
from type.jwt import TOKEN_TYPE_FIELD, REFRESH_TOKEN_TYPE, ACCESS_TOKEN_TYPE
from users.schemas import ResponseUser


@lru_cache(maxsize=1)
def get_private_key() -> str:
    return settings.auth.private_key.read_text()


@lru_cache(maxsize=1)
def get_public_key() -> str:
    return settings.auth.public_key.read_text()


def encode_jwt(
    payload: dict,
    private_key: str = get_private_key(),
    algorithm: str = settings.auth.algorithm,
    expire_minutes: int = settings.auth.access_token_expire_min,
    expire_timedelta: timedelta | None = None,
):
    now = datetime.now(timezone.utc)

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    payload.update(
        exp=int(expire.timestamp()),
        iat=int(now.timestamp()),
    )

    return jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=algorithm,
    )


def decode_jwt(
    token: str,
    public_key: str = get_public_key(),
    algorithm: str = settings.auth.algorithm,
):
    return jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    password_bytes: bytes = password.encode()
    hashed_password: bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password.encode(),
    )


def create_jwt(
    token_data: dict,
    token_type: str,
    expire_minutes: int = settings.auth.access_token_expire_min,
    expire_timedelta: timedelta | None = None,
) -> str:
    payload = {TOKEN_TYPE_FIELD: token_type}
    payload.update(token_data)
    return encode_jwt(
        payload=payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user_info: ResponseUser) -> str:
    payload = {
        "sub": str(user_info.id),
        "username": user_info.username,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=payload,
        expire_minutes=settings.auth.access_token_expire_min,
    )


def create_refresh_token(user_info: ResponseUser) -> str:
    payload = {
        "sub": str(user_info.id),
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=payload,
        expire_timedelta=timedelta(days=settings.auth.refresh_token_expire_days),
    )

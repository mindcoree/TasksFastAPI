import bcrypt
import jwt
from datetime import datetime, timezone, timedelta
from functools import lru_cache

from sqlalchemy.sql.coercions import expect

from core.config import settings


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
    expire_minute: int = settings.auth.expire_min,
):
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expire_minute)

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

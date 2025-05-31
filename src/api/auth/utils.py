import jwt
import bcrypt
from datetime import datetime, timezone, timedelta
from core.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth.private_key_path.read_text(),
    algorithm=settings.auth.algorithm,
    expire_minutes: int = settings.auth.access_token_expire_min,
):
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expire_minutes)

    payload.update(
        exp=int(expire.timestamp()),
        iat=int(now.timestamp()),
    )

    encoded = jwt.encode(
        payload,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token,
    public_key: str = settings.auth.public_key_path.read_text(),
    algorithms: str = settings.auth.algorithm,
):
    decoded = jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=[algorithms],
    )
    return decoded


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

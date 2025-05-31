import bcrypt


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

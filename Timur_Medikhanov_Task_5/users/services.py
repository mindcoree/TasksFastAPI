from fastapi import HTTPException, status, Request
from jwt.exceptions import InvalidTokenError
from utils import auth
from .models import User
from .repository import UserRepository
from .schemas import UserCreate, UserLogin, ResponseUser, TokenInfo
from anyio.to_thread import run_sync


class UserAuthService:
    def __init__(self, repository: UserRepository):
        self.repo = repository

    async def create_user(self, user_in: UserCreate) -> ResponseUser:
        hashed = await run_sync(auth.hash_password, user_in.password)
        user = await self.repo.create(username=user_in.username, password_hash=hashed)
        return ResponseUser(id=user.id, username=user.username)

    async def check_unique_user(self, check_user: UserCreate) -> UserCreate:
        existing_user = await self.repo.get_user(get_user=check_user)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username has already been taken.",
            )
        return check_user

    async def verify_credentials(self, sign_in_user: UserLogin) -> User:
        user = await self.repo.get_user(get_user=sign_in_user)
        if not user or not auth.verify_password(
            password=sign_in_user.password,
            hashed_password=user.password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        return user

    @staticmethod
    def get_current_user(request: Request) -> ResponseUser:
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No token provided",
            )
        try:
            payload = auth.decode_jwt(token=token)
            return ResponseUser(id=payload["sub"], username=payload["username"])
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )

    @staticmethod
    def sign_in(user_login: ResponseUser) -> TokenInfo:
        access_token = auth.create_access_token(user_info=user_login)
        refresh_token = auth.create_refresh_token(user_info=user_login)
        return TokenInfo(
            token=access_token,
            refresh=refresh_token,
            token_type="Cookie",
        )

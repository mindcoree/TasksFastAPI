from fastapi import HTTPException, status, Response
from jwt.exceptions import InvalidTokenError

from core.config import settings
from type.jwt import REFRESH_TOKEN_TYPE
from utils import auth
from .models import User
from .repository import UserRepository
from .schemas import UserCreate, UserLogin, ResponseUser, TokenInfo, UserSchemas

from .validations import validations_token_type


class UserAuthService:
    def __init__(self, repository: UserRepository):
        self.repo = repository

    async def create_user(self, user_in: UserCreate) -> UserSchemas:
        hashed = await auth.hash_password(password=user_in.password)
        user = await self.repo.create(username=user_in.username, password_hash=hashed)
        return UserSchemas(id=user.id, username=user.username, role=user.role)

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
        if not user or not await auth.verify_password(
            password=sign_in_user.password,
            hashed_password=user.password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        return user

    @staticmethod
    async def sign_in(user_login: UserLogin) -> TokenInfo:
        access_token = await auth.create_access_token(user_info=user_login)
        refresh_token = await auth.create_refresh_token(user_info=user_login)
        return TokenInfo(
            access=access_token,
            refresh=refresh_token,
            token_type="Cookie",
        )

    async def refresh_access_token_and_get_user(
        self,
        refresh_token: str,
        response: Response,
    ) -> User:
        try:
            payload = await auth.decode_jwt(refresh_token)
            await validations_token_type(token_type=REFRESH_TOKEN_TYPE, payload=payload)
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        user_id = int(payload.get("sub"))
        user = await self.repo.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        access_token = await auth.create_access_token(user_info=user)
        await auth.set_token_cookie(
            response=response,
            key="access_token",
            value=access_token,
            max_age=settings.auth.access_token_expire_min * 60,
        )

        return user

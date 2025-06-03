from fastapi import HTTPException, status, Response
from jwt import InvalidTokenError

from .repository import RepositoryUser
from .schemas import (
    UserCreate,
    UserLogin,
    TokenInfo,
    UserScheme,
    AdminCreate,
    AdminScheme,
    ResponseUser,
)
from .models import User, Role
from utils import auth
from core.config import settings


class UserAuthService:
    def __init__(self, repository: RepositoryUser):
        self.repo = repository

    async def create_user(self, user: UserCreate) -> UserScheme:
        hash_password = await auth.hash_password(user.password)
        user = await self.repo.create_user(user_in=user, hashed_password=hash_password)
        return user

    async def get_user(self, user_id: int) -> UserScheme:
        return await self.repo.get_user_by_id(user_id=user_id)

    async def create_admin(self, admin_info: AdminCreate) -> AdminScheme:
        hash_password = await auth.hash_password(admin_info.password)
        admin = await self.repo.create_admin(
            admin_in=admin_info, hashed_password=hash_password
        )
        return admin

    async def check_unique_user(self, check_user: UserCreate) -> UserCreate:
        existing_user: User = await self.repo.get_user_by_username(
            username=check_user.username
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username has already been taken.",
            )
        return check_user

    async def verify_credentials(self, credentials: UserLogin) -> User:
        user: User = await self.repo.get_user_by_username(username=credentials.username)
        if not user or not await auth.verify_password(
            password=credentials.password,
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
        return TokenInfo(access=access_token, refresh=refresh_token)

    async def refresh_access_token_and_get_user(
        self,
        response: Response,
        refresh_token: str,
    ):
        try:
            refresh_payload = await auth.decode_jwt(token=refresh_token)
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh-token.",
            )

        user_id = int(refresh_payload.get("sub"))
        user = await self.repo.get_user_by_id(user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
            )

        access_token = await auth.create_access_token(user_info=user)
        await auth.set_token_cookie(
            response=response,
            key="access_token",
            value=access_token,
            max_age=settings.auth.access_token_expire_min * 60,
        )

        return user

    async def get_list_user(self) -> UserScheme:
        return await self.repo.get_list_users()

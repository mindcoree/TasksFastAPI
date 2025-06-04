from typing import Generic
from jwt import InvalidTokenError
from core.config import settings
from utils import auth
from .repository import BaseRepository, T, BaseAuthRepository
from fastapi import HTTPException, status, Response, Request
from .enums import Role


class BaseService(Generic[T]):
    def __init__(self, repository: BaseRepository[T]):
        self.repo: BaseRepository[T] = repository

    async def create(self, **data) -> T:
        return await self.repo.create(**data)

    async def get_object_by_id(self, id_: int) -> T:
        instance = await self.repo.get_by_id(id_)
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{T} is not found by id: {id_} !",
            )
        return instance


class BaseAuthService(BaseService[T], Generic[T]):
    repo: BaseAuthRepository[T]

    def __init__(self, repository: BaseAuthRepository[T]):
        super().__init__(repository=repository)

    async def create(self, auth_info, role: Role) -> T:
        hash_password = await auth.hash_password(auth_info.password)
        instance = await super().create(
            login=auth_info.login,
            email=auth_info.email,
            hash_password=hash_password,
            role=role,
        )
        return instance

    async def verification_email(self, email: str) -> T | None:
        existing = await self.repo.get_by_email(email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email has already been taken.",
            )
        return True

    async def verification_login(self, login: str) -> T | None:
        existing = await self.repo.get_by_login(login)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="login has already been taken.",
            )
        return True

    async def verify_credentials(self, credentials) -> T:
        instance = await self.repo.get_instance_by_("login", credentials.login)
        if not instance or not await auth.verify_password(
            password=credentials.password,
            hashed_password=instance.hash_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        return instance

    async def refresh_access_token_and_get_user(
        self,
        response: Response,
        refresh_token: str,
    ) -> T:
        try:
            refresh_payload = await auth.decode_jwt(token=refresh_token)
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh-token.",
            )

        instance_id = int(refresh_payload.get("sub"))
        instance = await self.repo.get_by_id(id_=instance_id)
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="instance not found"
            )

        access_token = await auth.create_access_token(user_info=instance)
        await auth.set_token_cookie(
            response=response,
            key="access_token",
            value=access_token,
            max_age=settings.auth.access_expire_min * 60,
        )

        return instance

    async def access_token_payload(self, request: Request, response: Response) -> dict:
        payload = getattr(request.state, "user_payload", None)
        if payload:
            return payload

        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh-token is not provided",
            )

        instance = await self.refresh_access_token_and_get_user(
            response=response, refresh_token=refresh_token
        )
        payload = auth.create_payload(user_payload=instance)
        return payload

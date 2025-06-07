from typing import Generic
from jwt import InvalidTokenError
from core.config import settings
from utils import auth
from .repository import BaseRepository, T, BaseAuthRepository
from fastapi import HTTPException, status, Response, Request
from .enums import Role
from utils.auth import AccessTokenPayload


class BaseService(Generic[T]):
    def __init__(self, repository: BaseRepository[T], model: type[T]):
        self.repo: BaseRepository[T] = repository
        self.model = model

    @staticmethod
    async def ensure_unique(instance: T, field_name: str) -> None:
        if instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{field_name} already taken",
            )

    async def get_by_id(self, id_instance: int) -> T:
        return await self.repo.get_by_id(id_instance)

    async def ensure_instance_exists_by_id(self, id_instance) -> T:
        instance = await self.get_by_id(id_instance)
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} is not found by id: {id_instance} !",
            )
        return instance


class BaseAuthService(Generic[T]):
    def __init__(self, repository: BaseAuthRepository[T], model: type[T]):
        self.repo: BaseAuthRepository[T] = repository
        self.model = model

    async def create_auth(self, auth_in, role: Role) -> T:
        hash_password = await auth.hash_password(auth_in.password)
        data = auth_in.model_dump(exclude={"password"})
        data.update(
            {"hash_password": hash_password, "role": role},
        )
        return await self.repo.create(data)

    @staticmethod
    async def ensure_unique_verifications(instance: T, field_name: str):
        if instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{field_name} already taken",
            )
        return True

    async def verification_email(self, email: str) -> bool:
        existing = await self.repo.get_by_email(email)
        await self.ensure_unique_verifications(existing, field_name=email)

    async def verification_login(self, login: str) -> bool:
        existing = await self.repo.get_by_login(login)
        await self.ensure_unique_verifications(existing, field_name=login)

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

    async def refresh_access_token_and_get_auth(
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
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} not found by {instance_id}",
            )

        access_token = await auth.create_access_token(user_info=instance)
        await auth.set_token_cookie(
            response=response,
            key="access_token",
            value=access_token,
            max_age=settings.auth.access_expire_min * 60,
        )

        return instance

    async def access_token_payload(
        self, request: Request, response: Response
    ) -> AccessTokenPayload:
        payload = getattr(request.state, "user_payload", None)
        if payload:
            return AccessTokenPayload(**payload)

        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is not provided",
            )

        instance = await self.refresh_access_token_and_get_auth(
            response=response, refresh_token=refresh_token
        )
        payload = auth.create_payload(user_payload=instance)
        return AccessTokenPayload(**payload)

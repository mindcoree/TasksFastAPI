from src.api.users.repository import UserRepository
from src.api.users.service import UserService
from src.core.db_helper import db_helper
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

SessionDep = Annotated[AsyncSession, Depends(db_helper.session_getter)]


def get_user_service(session: SessionDep) -> UserService:
    repo = UserRepository(session)
    return UserService(repository=repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]

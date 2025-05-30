from .repository import UserRepository
from .service import UserService
from core.db_helper import db_helper
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

SessionDep = Annotated[AsyncSession, Depends(db_helper.session_getter)]


def get_user_service(session: SessionDep) -> UserService:
    repo = UserRepository(session)
    return UserService(repository=repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]

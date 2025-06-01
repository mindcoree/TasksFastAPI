from .repository import UserRepository
from .service import UserService
from typing import Annotated
from fastapi import Depends, Form, HTTPException, status, Request
from sqlalchemy import select, Result
from .schemas import UserCreate, UserLogin, ResponseUser
from utils import auth
from .models import User
from core.db_helper import SessionDep
from jwt.exceptions import InvalidTokenError
from api.users import repository as repo


def get_user_service(session: SessionDep) -> UserService:
    repos = UserRepository(session)
    return UserService(repository=repos)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]

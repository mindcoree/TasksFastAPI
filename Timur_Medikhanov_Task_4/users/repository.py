from sqlalchemy import select, Result
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from utils import auth
from .schemas import UserLogin, ResponseUser, UserCreate, AccessToken
from .models import User


async def create_users(session: AsyncSession, user_in: UserCreate) -> ResponseUser:
    hash_password = auth.hash_password(user_in.password)
    new_user = User(username=user_in.username, password=hash_password)
    session.add(new_user)
    await session.commit()
    return ResponseUser(id=new_user.id, username=new_user.username)


async def sing_in(user_login: ResponseUser) -> AccessToken:
    payload = {
        "sub": user_login.id,
        "username": user_login.username,
    }
    token = auth.encode_jwt(payload=payload)
    return AccessToken(token=token, token_type="Bearer")

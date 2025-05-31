from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.users.schemas import UserScheme
from api.auth.utils import encode_jwt

router = APIRouter(prefix="/auth", tags=["auth"])


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


def validate_auth_login():
    pass


@router.post("/login", response_model=TokenInfo)
async def auth_issue_jwt(user: UserScheme = Depends(validate_auth_login)):

    payload = {
        "sub": user.username,
        **user.model_dump(),
    }

    token = encode_jwt(payload)

    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )

from type.jwt import TOKEN_TYPE_FIELD
from fastapi import HTTPException, status


async def validations_token_type(token_type: str, payload: dict) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type != token_type:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="invalid token type",
        )
    return True

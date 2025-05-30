from typing import Annotated

from fastapi import APIRouter,Header

router = APIRouter(tags=['dependencies'])


@router.get("/single-direct-dependency")
async def single_direct_dependency(
        foobar: Annotated[str,Header]
):
    return {
        "foobar":foobar,
        "message":"single-direct-dependency"
    }

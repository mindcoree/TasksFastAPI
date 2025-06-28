from typing import Annotated

from fastapi import APIRouter, Form

from core.config import settings
from .dependencies import AdminAuthServiceDep
from .schemas import AdminCreate, AdminInfo

router = APIRouter(prefix=settings.api.members.admin.prefix, tags=["ADMIN"])


@router.post("/create", response_model=AdminInfo)
async def create(
    admin: Annotated[AdminCreate, Form()],
    service: AdminAuthServiceDep,
) -> AdminInfo:
    return await service.create_admin(admin_in=admin)

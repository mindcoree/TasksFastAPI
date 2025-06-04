from fastapi import APIRouter
from core.config import settings
from .members import router as members_router


router = APIRouter(prefix=settings.api.prefix)


router.include_router(members_router)

from fastapi import APIRouter
from core.config import settings
from .users.views import router as users_router
from .admins.views import router as admins_router

router = APIRouter(prefix=settings.api.members.prefix)


router.include_router(users_router)
router.include_router(admins_router)

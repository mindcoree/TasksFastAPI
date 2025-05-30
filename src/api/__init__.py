from fastapi import APIRouter
from .users.views import router as router_users
from core.config import settings
from .auth.views import router as router_auth

router = APIRouter()

router.include_router(router_users, prefix=settings.api.users.prefix)
router.include_router(router_auth)

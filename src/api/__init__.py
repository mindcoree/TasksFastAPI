from fastapi import APIRouter
from users.views import router as router_users
from core.config import settings

router = APIRouter()

router.include_router(router_users,prefix=settings.api.users.prefix)
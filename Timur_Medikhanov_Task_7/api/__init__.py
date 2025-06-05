from fastapi import APIRouter
from core.config import settings
from .members import router as members_router
from .products.views import router as products_router

router = APIRouter(prefix=settings.api.prefix)


router.include_router(members_router)
router.include_router(products_router)

from fastapi import APIRouter
from core.config import settings
from note.views import router as router_note


router = APIRouter(prefix=settings.api.note.prefix)


router.include_router(router_note, prefix=settings.api.note.prefix)

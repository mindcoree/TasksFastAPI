from fastapi import APIRouter
from Timur_Medikhanov_Task_16.core.config import settings
from Timur_Medikhanov_Task_16.api.note.views import router as router_note


router = APIRouter()


router.include_router(router_note, prefix=settings.api.note.prefix)

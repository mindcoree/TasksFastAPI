from fastapi import APIRouter
from core.config import settings

router = APIRouter(prefix=settings.api.bk.prefix, tags=["BANK-ACCOUNT"])

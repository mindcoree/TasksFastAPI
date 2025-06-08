from fastapi import APIRouter

from core.config import settings

router = APIRouter(prefix=settings.api.orders.prefix, tags=["ORDERS"])

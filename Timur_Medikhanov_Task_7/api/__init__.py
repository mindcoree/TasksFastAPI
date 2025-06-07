from fastapi import APIRouter
from core.config import settings
from .members import router as members_router
from .products.views import router as products_router
from .orders.views import router as orders_router

# Импорт моделей для инициализации SQLAlchemy-схем
from api.members.models import Member
from api.orders.models import Order
from api.products.models import Product
from api.common.order_product_association import OrderProductAssociation


router = APIRouter(prefix=settings.api.prefix)


router.include_router(members_router)
router.include_router(products_router)
router.include_router(orders_router)

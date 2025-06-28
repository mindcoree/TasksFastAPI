from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from .repository import OrderRepository
from .schemas import OrderCreate
from .models import Order
from .exceptions import OrderInvalidData
from ..products.exceptions import ProductNotFoundId


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session
        self.repo = OrderRepository(self.session)

    async def create_order_with_products(
        self, order_data: OrderCreate, member_id: int
    ) -> Order:
        order = await self.repo.create_order(order_data, member_id)

        total_amount = Decimal("0.00")

        for product_data in order_data.products:
            product = await self.repo.product_by_id(id_product=product_data.product_id)

            if product is None:
                raise ProductNotFoundId(product_data.product_id)

            if product.stock < product_data.quantity:
                raise OrderInvalidData(
                    f"Not enough stock for {product.name}. Available: {product.stock}"
                )

            await self.repo.create_order_with_product(
                order_product_info=product_data,
                product=product,
                order=order,
            )

            position_price = product.price * product_data.quantity
            product.stock -= product_data.quantity
            total_amount += position_price

        order.total_amount = total_amount
        await self.session.commit()
        await self.session.refresh(order)
        return order

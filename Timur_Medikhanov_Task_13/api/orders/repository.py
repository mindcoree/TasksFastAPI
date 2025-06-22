from sqlalchemy.ext.asyncio import AsyncSession
from ..common.order_product_association import OrderProductAssociation
from .models import Order
from ..products.models import Product
from .schemas import OrderCreate, OrderProductCreate
from ..products.repository import ProductRepository


class OrderRepository(ProductRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.session = session

    async def create_order(
        self,
        order_data: OrderCreate,
        member_id: int,
    ) -> Order:
        order = Order(
            member_id=member_id,
            shipping_address=order_data.shipping_address,
        )
        self.session.add(order)
        return order

    async def create_order_with_product(
        self,
        order_product_info: OrderProductCreate,
        product: Product,
        order,
    ) -> OrderProductAssociation:
        order_product_association = OrderProductAssociation(
            order_id=order.id,
            product_id=product.id,
            quantity=order_product_info.quantity,
            unit_price=product.price,
        )
        self.session.add(order_product_association)
        return order_product_association

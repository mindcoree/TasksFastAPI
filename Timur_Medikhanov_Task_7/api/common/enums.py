from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"


class OrderStatus(str, Enum):
    PENDING = "pending"  # заказа создан, но не обработан
    PROCESSING = "processing"  # в обработке
    SHIPPED = "shipped"  # Отправлен
    DELIVERED = "delivered"  # Доставлен
    CANCELLED = "cancelled"  # Отменен


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"

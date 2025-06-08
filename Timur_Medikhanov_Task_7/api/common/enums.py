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


# Банки
class BankName(str, Enum):
    SBERBANK = "sberbank"
    TINKOFF = "tinkoff"
    ALFABANK = "alfabank"
    HOMECREDIT = "homecredit"


# Платёжные системы
class PaymentSystem(str, Enum):
    VISA = "visa"
    MASTERCARD = "mastercard"
    MIR = "mir"


class AccountStatus(str, Enum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    EXPIRED = "EXPIRED"

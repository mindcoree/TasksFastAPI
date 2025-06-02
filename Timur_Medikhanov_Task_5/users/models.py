from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from core.base import Base
from enum import Enum


class Role(str, Enum):
    admin = "admin"
    user = "user"
    guest = "guest"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    role: Mapped[Role] = mapped_column(
        server_default=expression.literal("guest"), default=Role.guest
    )

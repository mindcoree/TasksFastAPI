from sqlalchemy.orm import Mapped, mapped_column
from core.base import Base
from enum import Enum


class Role(str, Enum):
    guest = "guest"
    user = "user"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    role: Mapped[Role]

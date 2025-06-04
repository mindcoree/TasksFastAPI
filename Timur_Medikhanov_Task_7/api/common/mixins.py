from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from api.common.enums import Role
from type.annotated import created_at, updated_at


class BaseAccountMixin:
    __abstract__ = True

    login: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    hash_password: Mapped[str]
    role: Mapped[Role]


class TimestampMix:
    __abstract__ = True

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

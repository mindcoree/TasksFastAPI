from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, declared_attr, relationship

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


if TYPE_CHECKING:
    from api.members.models import Member


class MemberRelationMix:
    __member_id_unique__: bool = False  # для связей o2o
    __member_nullable__: bool = False
    __member_back_populates: str | None = None

    @declared_attr
    def member_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey(
                "members.id",
                ondelete="CASCADE",
            ),
            nullable=cls.__member_nullable__,
            unique=cls.__member_id_unique__,
        )

    @declared_attr
    def member(cls) -> Mapped["Member"]:
        return relationship("Member", back_populates=cls.__member_back_populates)

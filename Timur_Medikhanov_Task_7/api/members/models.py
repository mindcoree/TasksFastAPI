from api.common.base import Base
from api.common.mixins import BaseAccountMixin
from sqlalchemy.orm import Mapped, mapped_column
from type.annotated import ID_PK


class Members(BaseAccountMixin, Base):
    __tablename__ = "members"

    id: Mapped[ID_PK]
    email: Mapped[str] = mapped_column(nullable=False, unique=True)

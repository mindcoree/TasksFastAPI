from api.common.base import Base
from type.annotated import ID_PK
from sqlalchemy.orm import Mapped


class Admin(Base):
    id: Mapped[ID_PK]

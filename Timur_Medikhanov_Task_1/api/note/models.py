from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from Timur_Medikhanov_Task_1.core.base import Base


class Note(Base):
    __tablename__ = "notes"

    text: Mapped[str]
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

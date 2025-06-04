from datetime import datetime
from typing import Annotated
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func
from pydantic import Field, StringConstraints

ID_PK = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=func.now(),
        nullable=False,
    ),
]

updated_at = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
    ),
]


login = Annotated[
    str,
    Field(
        min_length=8,
        max_length=40,
        description="Login must be between 8 and 40 characters.",
        examples=["mindcore"],
    ),
]

password = Annotated[
    str,
    StringConstraints(
        min_length=8,
        max_length=40,
        pattern=r"^[A-Za-z\d@$!%*#?&]+$",
    ),
]

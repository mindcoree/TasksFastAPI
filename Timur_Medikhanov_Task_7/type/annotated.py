from datetime import datetime
from typing import Annotated, Type


from sqlalchemy.orm import mapped_column
from sqlalchemy import DateTime, func, JSON
from pydantic import Field, StringConstraints, BaseModel
from fastapi import Form, Query


def form_model(schema: Type[BaseModel]) -> type[BaseModel]:
    """Wraps a Pydantic model with Form dependency for FastAPI."""
    return Annotated[schema, Form()]


def query_model(schema: Type[BaseModel]) -> type[BaseModel]:
    return Annotated[schema, Query()]


ID_PK: type[int] = Annotated[int, mapped_column(primary_key=True)]
JSON = Annotated[dict, mapped_column(JSON)]


created_at = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    ),
]

updated_at = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
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

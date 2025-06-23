from datetime import datetime

from pydantic import BaseModel


class NoteBase(BaseModel):
    text: str


class NoteCreate(NoteBase):
    pass


class NoteOut(NoteBase):
    id: int
    create_at: datetime

from sqlalchemy import select
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from Timur_Medikhanov_Task_16.api.note.models import Note
from Timur_Medikhanov_Task_16.api.note.schemas import NoteCreate


class NotesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list_notes(self) -> Sequence[Note]:
        stms = select(Note).order_by(Note.id)
        result = await self.session.scalars(stms)
        return result.all()

    async def create_notes(self, note_in: NoteCreate) -> Note:
        create_note = Note(**note_in.model_dump())
        self.session.add(create_note)
        await self.session.commit()
        await self.session.refresh(create_note)
        return create_note

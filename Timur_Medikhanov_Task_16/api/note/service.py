from Timur_Medikhanov_Task_16.api.note.repository import NotesRepository
from typing import Sequence
from Timur_Medikhanov_Task_16.api.note.schemas import NoteCreate, NoteOut


class NotesService:
    def __init__(self, repository: NotesRepository):
        self.repo: NotesRepository = repository

    async def get_list_notes(self) -> Sequence[NoteOut]:
        notes = await self.repo.get_list_notes()
        return notes

    async def create_notes(self, note_in) -> NoteCreate:
        create_note = await self.repo.create_notes(note_in)
        return create_note

from typing import Sequence

from fastapi import APIRouter
from Timur_Medikhanov_Task_1.core.config import settings
from Timur_Medikhanov_Task_1.api.note.schemas import NoteOut, NoteCreate
from Timur_Medikhanov_Task_1.api.note.dependencies import ServiceDep

router = APIRouter(tags=["Note"])


@router.get("/notes", response_model=Sequence[NoteOut])
async def get_list_notes(service: ServiceDep) -> Sequence[NoteOut]:
    notes = await service.get_list_notes()
    return notes


@router.post("/notes", response_model=NoteOut)
async def create_note(note_in: NoteCreate, service: ServiceDep) -> NoteOut:
    return await service.create_notes(note_in=note_in)

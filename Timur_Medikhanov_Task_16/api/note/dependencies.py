from Timur_Medikhanov_Task_16.core.db_helper import db_helper
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from Timur_Medikhanov_Task_16.api.note.service import NotesService
from Timur_Medikhanov_Task_16.api.note.repository import NotesRepository


SessionDep = Annotated[AsyncSession, Depends(db_helper.session_getter)]


def get_note_service(session: SessionDep) -> NotesService:
    repo = NotesRepository(session=session)
    return NotesService(repository=repo)


ServiceDep = Annotated[NotesService, Depends(get_note_service)]

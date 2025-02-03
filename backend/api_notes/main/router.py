from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api_notes.main.schemas import NotesCreate, NotesResponse
from backend.api_notes.main.service import NotesService
from backend.settings.database import get_db
from uuid import UUID

router = APIRouter(prefix="/api/notes/main")

@router.post("/create/", response_model=NotesResponse)
async def create_notes(notes: NotesCreate, db: get_db = Depends()):
    result = NotesService(db).create_notes(notes)
    return result

@router.get("/list/", response_model=list[NotesResponse])
async def read_notes(db: get_db = Depends()):
    result = NotesService(db).get_notes()
    return result

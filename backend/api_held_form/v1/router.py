from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api_held_form.v1.schemas import HeldFormCreate, HeldFormUpdate, HeldFormResponse
from backend.api_held_form.v1.service import HeldFormService
from backend.settings.database import get_db
from uuid import UUID

router = APIRouter(prefix="/api/held_forms/temp")

@router.post("/create/", response_model=HeldFormResponse)
async def create_held_form(held_form: HeldFormCreate, db: get_db = Depends()):
    result = HeldFormService(db).create_held_form(held_form)
    return result

@router.get("/list/", response_model=list[HeldFormResponse])
async def read_held_form(db: get_db = Depends()):
    result = HeldFormService(db).get_held_form()
    return result

@router.put("/update/{held_form_id}/", response_model=HeldFormResponse)
async def update_held_form(held_form_id: UUID, held_form_update: HeldFormUpdate, db: get_db = Depends()):
    result = HeldFormService(db).update_held_form(held_form_id, held_form_update)
    return result

@router.put("/restore/{held_form_id}/", response_model=HeldFormResponse)
async def restore_held_form(held_form_id: UUID,  db: get_db = Depends()):
    result = HeldFormService(db).restore_held_form(held_form_id)
    return result

@router.delete("/delete/{held_form_id}/", response_model=HeldFormResponse)
async def delete_held_form(held_form_id: UUID, db: get_db = Depends()):
    result = HeldFormService(db).soft_delete_held_form(held_form_id)
    return result


from fastapi import APIRouter, Depends
from backend.api_held_form.temp.schemas import TempHeldFormCreate, TempHeldFormUpdate, TempHeldFormResponse, TempHeldForm
from backend.api_held_form.temp.service import TempHeldFormService
from backend.settings.database import get_db
from uuid import UUID

router = APIRouter(prefix="/api/held_forms/temp")

@router.post("/create/", response_model=TempHeldForm)
async def create_held_form(held_form: TempHeldFormCreate, db: get_db = Depends()):
    result = TempHeldFormService(db).create_held_form(held_form)
    return result

@router.get("/list/", response_model=list[TempHeldFormResponse])
async def read_held_form(db: get_db = Depends()):
    result = TempHeldFormService(db).get_held_form()
    return result

@router.put("/update/{held_form_id}/", response_model=list[TempHeldFormResponse])
async def update_held_form(held_form_id: UUID, held_form_update: TempHeldFormUpdate, db: get_db = Depends()):
    result = TempHeldFormService(db).update_held_form(held_form_id, held_form_update)
    return result

@router.put("/restore/{held_form_id}/", response_model=TempHeldFormResponse)
async def restore_held_form(held_form_id: UUID,  db: get_db = Depends()):
    result = TempHeldFormService(db).restore_held_form(held_form_id)
    return result

@router.delete("/delete/{held_form_id}/", response_model=list[TempHeldFormResponse])
async def delete_held_form(held_form_id: UUID, db: get_db = Depends()):
    result = TempHeldFormService(db).soft_delete_held_form(held_form_id)
    return result


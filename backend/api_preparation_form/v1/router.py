from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api_preparation_form.v1.schemas import PreparationFormCreate, PreparationFormUpdate, PreparationFormResponse
from backend.api_preparation_form.v1.service import PreparationFormService
from backend.settings.database import get_db
from uuid import UUID

router = APIRouter(prefix="/api/preparation_forms/temp")

@router.post("/create/", response_model=PreparationFormResponse)
async def create_preparation_form(preparation_form: PreparationFormCreate, db: get_db = Depends()):
    result = PreparationFormService(db).create_preparation_form(preparation_form)
    return result

@router.get("/list/", response_model=list[PreparationFormResponse])
async def read_preparation_form(db: get_db = Depends()):
    result = PreparationFormService(db).get_preparation_form()
    return result

@router.put("/update/{preparation_form_id}/", response_model=PreparationFormResponse)
async def update_preparation_form(preparation_form_id: UUID, preparation_form_update: PreparationFormUpdate, db: get_db = Depends()):
    result = PreparationFormService(db).update_preparation_form(preparation_form_id, preparation_form_update)
    return result

@router.put("/restore/{preparation_form_id}/", response_model=PreparationFormResponse)
async def restore_preparation_form(preparation_form_id: UUID,  db: get_db = Depends()):
    result = PreparationFormService(db).restore_preparation_form(preparation_form_id)
    return result

@router.delete("/delete/{preparation_form_id}/", response_model=PreparationFormResponse)
async def delete_preparation_form(preparation_form_id: UUID, db: get_db = Depends()):
    result = PreparationFormService(db).soft_delete_preparation_form(preparation_form_id)
    return result


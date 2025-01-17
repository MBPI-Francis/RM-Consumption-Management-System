from fastapi import APIRouter, Depends
from backend.api_preparation_form.temp.schemas import TempPreparationFormCreate, TempPreparationFormUpdate, TempPreparationFormResponse
from backend.api_preparation_form.temp.service import TempPreparationFormService
from backend.settings.database import get_db
from uuid import UUID

router = APIRouter(prefix="/api/preparation_forms/temp")

@router.post("/create/", response_model=TempPreparationFormResponse)
async def create_preparation_form(preparation_form: TempPreparationFormCreate, db: get_db = Depends()):
    result = TempPreparationFormService(db).create_preparation_form(preparation_form)
    return result

@router.get("/list/", response_model=list[TempPreparationFormResponse])
async def read_preparation_form(db: get_db = Depends()):
    result = TempPreparationFormService(db).get_preparation_form()
    return result

@router.put("/update/{preparation_form_id}/", response_model=TempPreparationFormResponse)
async def update_preparation_form(preparation_form_id: UUID, preparation_form_update: TempPreparationFormUpdate, db: get_db = Depends()):
    result = TempPreparationFormService(db).update_preparation_form(preparation_form_id, preparation_form_update)
    return result

@router.put("/restore/{preparation_form_id}/", response_model=TempPreparationFormResponse)
async def restore_preparation_form(preparation_form_id: UUID,  db: get_db = Depends()):
    result = TempPreparationFormService(db).restore_preparation_form(preparation_form_id)
    return result

@router.delete("/delete/{preparation_form_id}/", response_model=TempPreparationFormResponse)
async def delete_preparation_form(preparation_form_id: UUID, db: get_db = Depends()):
    result = TempPreparationFormService(db).soft_delete_preparation_form(preparation_form_id)
    return result


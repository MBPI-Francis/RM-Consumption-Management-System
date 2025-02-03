from fastapi import APIRouter, Depends
from backend.api_preparation_form.main.schemas import PreparationFormCreate, PreparationFormResponse
from backend.api_preparation_form.main.service import PreparationFormService
from backend.settings.database import get_db
from uuid import UUID

router = APIRouter(prefix="/api/preparation_forms/main")

@router.post("/create/", response_model=PreparationFormResponse)
async def create_preparation_form(preparation_form: PreparationFormCreate, db: get_db = Depends()):
    result = PreparationFormService(db).create_preparation_form(preparation_form)
    return result

@router.get("/list/", response_model=list[PreparationFormResponse])
async def read_preparation_form(db: get_db = Depends()):
    result = PreparationFormService(db).get_preparation_form()
    return result
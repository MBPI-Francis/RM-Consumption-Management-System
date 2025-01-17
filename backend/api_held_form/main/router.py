from fastapi import APIRouter, Depends

from backend.api_held_form.main.schemas import HeldFormCreate, HeldFormResponse
from backend.api_held_form.main.service import HeldFormService
from backend.settings.database import get_db


router = APIRouter(prefix="/api/held_forms/main")

@router.post("/create/", response_model=HeldFormResponse)
async def create_held_form(held_form: HeldFormCreate, db: get_db = Depends()):
    result = HeldFormService(db).create_held_form(held_form)
    return result

@router.get("/list/", response_model=list[HeldFormResponse])
async def read_held_form(db: get_db = Depends()):
    result = HeldFormService(db).get_held_form()
    return result

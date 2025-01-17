from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api_transfer_form.main.schemas import TransferFormCreate, TransferFormResponse
from backend.api_transfer_form.main.service import TransferFormService
from backend.settings.database import get_db

router = APIRouter(prefix="/api/transfer_forms/main")

@router.post("/create/", response_model=TransferFormResponse)
async def create_transfer_form(transfer_form: TransferFormCreate, db: get_db = Depends()):
    result = TransferFormService(db).create_transfer_form(transfer_form)
    return result

@router.get("/list/", response_model=list[TransferFormResponse])
async def read_transfer_form(db: get_db = Depends()):
    result = TransferFormService(db).get_transfer_form()
    return result



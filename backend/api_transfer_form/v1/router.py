from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api_transfer_form.v1.schemas import TransferFormCreate, TransferFormUpdate, TransferFormResponse
from backend.api_transfer_form.v1.service import TransferFormService
from backend.settings.database import get_db
from uuid import UUID

router = APIRouter(prefix="/api/transfer_forms/v1")

@router.post("/create/", response_model=TransferFormResponse)
async def create_transfer_form(transfer_form: TransferFormCreate, db: get_db = Depends()):
    result = TransferFormService(db).create_transfer_form(transfer_form)
    return result

@router.get("/list/", response_model=list[TransferFormResponse])
async def read_transfer_form(db: get_db = Depends()):
    result = TransferFormService(db).get_transfer_form()
    return result

@router.put("/update/{transfer_form_id}/", response_model=TransferFormResponse)
async def update_transfer_form(transfer_form_id: UUID, transfer_form_update: TransferFormUpdate, db: get_db = Depends()):
    result = TransferFormService(db).update_transfer_form(transfer_form_id, transfer_form_update)
    return result

@router.put("/restore/{transfer_form_id}/", response_model=TransferFormResponse)
async def restore_transfer_form(transfer_form_id: UUID,  db: get_db = Depends()):
    result = TransferFormService(db).restore_transfer_form(transfer_form_id)
    return result

@router.delete("/delete/{transfer_form_id}/", response_model=TransferFormResponse)
async def delete_transfer_form(transfer_form_id: UUID, db: get_db = Depends()):
    result = TransferFormService(db).soft_delete_transfer_form(transfer_form_id)
    return result


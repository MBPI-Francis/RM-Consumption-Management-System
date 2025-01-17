from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api_stock_on_hand.v1.schemas import StockOnHandCreate, StockOnHandUpdate, StockOnHandResponse
from backend.api_stock_on_hand.v1.service import StockOnHandService
from backend.settings.database import get_db
from uuid import UUID

router = APIRouter(prefix="/api/rm_stock_on_hand/temp")

@router.post("/create/", response_model=StockOnHandResponse)
async def create_rm_soh(rm_soh: StockOnHandCreate, db: get_db = Depends()):
    result = StockOnHandService(db).create_rm_soh(rm_soh)
    return result

@router.get("/list/", response_model=list[StockOnHandResponse])
async def read_rm_soh(db: get_db = Depends()):
    result = StockOnHandService(db).get_rm_soh()
    return result

@router.put("/update/{rm_soh_id}/", response_model=StockOnHandResponse)
async def update_rm_soh(rm_soh_id: UUID, rm_soh_update: StockOnHandUpdate, db: get_db = Depends()):
    result = StockOnHandService(db).update_rm_soh(rm_soh_id, rm_soh_update)
    return result


@router.put("/restore/{rm_soh_id}/", response_model=StockOnHandResponse)
async def restore_rm_soh(rm_soh_id: UUID,  db: get_db = Depends()):
    result = StockOnHandService(db).restore_rm_soh(rm_soh_id)
    return result


@router.delete("/delete/{rm_soh_id}/", response_model=StockOnHandResponse)
async def delete_rm_soh(rm_soh_id: UUID, db: get_db = Depends()):
    result = StockOnHandService(db).soft_delete_rm_soh(rm_soh_id)
    return result
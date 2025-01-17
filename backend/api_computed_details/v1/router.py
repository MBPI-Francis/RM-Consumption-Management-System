from fastapi import APIRouter, Depends
from backend.api_computed_details.v1.schemas import ComputedDetailCreate, ComputedDetailResponse
from backend.api_computed_details.v1.service import ComputedDetailService
from backend.settings.database import get_db
from uuid import UUID
from datetime import datetime

router = APIRouter(prefix="/api/computed_details/")

@router.post("/create/", response_model=ComputedDetailResponse)
async def create_computed_detail(computed_detail: ComputedDetailCreate, db: get_db = Depends()):
    result = ComputedDetailService(db).create_computed_detail(computed_detail)
    return result

@router.get("/list/", response_model=list[ComputedDetailResponse])
async def read_computed_detail(db: get_db = Depends()):
    result = ComputedDetailService(db).list_computed_detail()
    return result

@router.get("/get/{computed_date}/{computed_by_id}/", response_model=list[ComputedDetailResponse])
async def read_computed_detail(computed_date: datetime,computed_by_id: UUID,db: get_db = Depends()):
    result = ComputedDetailService(db).get_computed_detail(computed_date, computed_by_id)
    return result

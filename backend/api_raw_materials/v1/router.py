from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api_raw_materials.v1.schemas import RawMaterialCreate, RawMaterialUpdate, RawMaterialResponse
from backend.api_raw_materials.v1.service import RawMaterialService
from backend.settings.database import get_db
from uuid import UUID

router = APIRouter(prefix="/api/raw_materials/v1")

@router.post("/create/", response_model=RawMaterialResponse)
async def create_raw_material(raw_material: RawMaterialCreate, db: get_db = Depends()):
    result = RawMaterialService(db).create_raw_material(raw_material)
    return result

@router.get("/list/", response_model=list[RawMaterialResponse])
async def read_raw_material(db: get_db = Depends()):
    result = RawMaterialService(db).get_raw_material()
    return result

@router.put("/update/{rm_id}/", response_model=RawMaterialResponse)
async def update_raw_material(rm_id: UUID, raw_material_update: RawMaterialUpdate, db: get_db = Depends()):
    result = RawMaterialService(db).update_raw_material(rm_id, raw_material_update)
    return result


@router.put("/restore/{rm_id}/", response_model=RawMaterialResponse)
async def restore_raw_material(rm_id: UUID,  db: get_db = Depends()):
    result = RawMaterialService(db).restore_raw_material(rm_id)
    return result


@router.delete("/delete/{rm_id}/", response_model=RawMaterialResponse)
async def delete_raw_material(rm_id: UUID, db: get_db = Depends()):
    result = RawMaterialService(db).soft_delete_raw_material(rm_id)
    return result
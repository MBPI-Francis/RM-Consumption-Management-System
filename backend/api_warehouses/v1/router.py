from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api_warehouses.v1.schemas import WarehouseCreate, WarehouseUpdate, WarehouseResponse
from backend.api_warehouses.v1.service import WarehouseService
from backend.settings.database import get_db
from uuid import UUID

router = APIRouter(prefix="/api/warehouses/v1")

@router.post("/create/", response_model=WarehouseResponse)
async def create_warehouse(department: WarehouseCreate, db: get_db = Depends()):
    result = WarehouseService(db).create_warehouse(department)
    return result

@router.get("/list/", response_model=list[WarehouseResponse])
async def read_warehouse(db: get_db = Depends()):
    result = WarehouseService(db).get_warehouse()
    return result

@router.put("/update/{warehouse_id}/", response_model=WarehouseResponse)
async def update_warehouse(warehouse_id: UUID, user_update: WarehouseUpdate, db: get_db = Depends()):
    result = WarehouseService(db).update_warehouse(warehouse_id, user_update)
    return result


@router.put("/restore/{warehouse_id}/", response_model=WarehouseResponse)
async def restore_warehouse(warehouse_id: UUID,  db: get_db = Depends()):
    result = WarehouseService(db).restore_warehouse(warehouse_id)
    return result


@router.delete("/delete/{warehouse_id}/", response_model=WarehouseResponse)
async def deactivate_warehouse(warehouse_id: UUID, db: get_db = Depends()):
    result = WarehouseService(db).soft_delete_warehouse(warehouse_id)
    return result
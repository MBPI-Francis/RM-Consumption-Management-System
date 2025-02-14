from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api_droplist.v1.schemas import DropListCreate, DropListUpdate, DropListResponse
from backend.api_droplist.v1.service import DropListService
from backend.settings.database import get_db
from uuid import UUID

router = APIRouter(prefix="/api/droplist")

@router.post("/create/", response_model=DropListResponse)
async def create_droplist(droplist: DropListCreate, db: get_db = Depends()):
    result = DropListService(db).create_droplist(droplist)
    return result

@router.get("/list/", response_model=list[DropListResponse])
async def read_droplist(db: get_db = Depends()):
    result = DropListService(db).get_droplist()
    return result

@router.get("/get/good/status/", response_model=list[DropListResponse])
async def read_droplist(db: get_db = Depends()):
    result = DropListService(db).get_good_status()
    return result

@router.put("/update/{droplist_id}/", response_model=DropListResponse)
async def update_droplist(droplist_id: UUID, droplist_update: DropListUpdate, db: get_db = Depends()):
    result = DropListService(db).update_droplist(droplist_id, droplist_update)
    return result

@router.put("/restore/{droplist_id}/", response_model=DropListResponse)
async def restore_droplist(droplist_id: UUID,  db: get_db = Depends()):
    result = DropListService(db).restore_droplist(droplist_id)
    return result


@router.delete("/delete/{droplist_id}/", response_model=DropListResponse)
async def delete_droplist(droplist_id: UUID, db: get_db = Depends()):
    result = DropListService(db).soft_delete_droplist(droplist_id)
    return result
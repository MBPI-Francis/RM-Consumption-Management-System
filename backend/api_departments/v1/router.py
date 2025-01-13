from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api_departments.v1.schemas import DepartmentCreate, DepartmentResponse, DepartmentUpdate
from backend.api_departments.v1.service import DepartmentService
from backend.settings.database import get_db
from uuid import UUID

router = APIRouter(prefix="/departments/v1")

@router.post("/create/", response_model=DepartmentResponse)
async def create_department(department: DepartmentCreate, db: get_db = Depends()):
    result = DepartmentService(db).create_department(department)
    return result

@router.get("/list/", response_model=list[DepartmentResponse])
async def read_departments(db: get_db = Depends()):
    result = DepartmentService(db).get_department()
    return result

@router.put("/update/{department_id}/", response_model=DepartmentResponse)
async def update_department(department_id: UUID, department_update: DepartmentUpdate, db: get_db = Depends()):
    result = DepartmentService(db).update_department(department_id, department_update)
    return result


@router.put("/restore/{department_id}/", response_model=DepartmentResponse)
async def restore_department(department_id: UUID,  db: get_db = Depends()):
    result = DepartmentService(db).restore_department(department_id)
    return result


@router.delete("/delete/{department_id}/", response_model=DepartmentResponse)
async def soft_delete_department(department_id: UUID, db: get_db = Depends()):
    result = DepartmentService(db).soft_delete_department(department_id)
    return result
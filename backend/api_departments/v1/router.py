from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api_departments.v1.schemas import DepartmentCreate, DepartmentResponse
from backend.api_departments.v1.service import DepartmentService
from backend.api_departments.v1.service_result import handle_result
from backend.settings.database import get_db

router = APIRouter(prefix="/departments/v1")

@router.post("/create/", response_model=DepartmentResponse)
async def create_department(department: DepartmentCreate, db: get_db = Depends()):
    result = DepartmentService(db).create_department(department)
    return result

@router.get("/list/", response_model=list[DepartmentResponse])
async def read_departments(db: get_db = Depends()):
    result = DepartmentService(db).get_department()
    return handle_result(result)


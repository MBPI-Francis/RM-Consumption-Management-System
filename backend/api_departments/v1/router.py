from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api_departments.v1.schemas import DepartmentCreate, DepartmentResponse
from backend.api_departments.v1.service import create_department_service, get_departments_service
from backend.settings.database import get_db

router = APIRouter(prefix="/departments/v1")

@router.post("/create", response_model=DepartmentResponse)
async def create_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    return create_department_service(db, department)

@router.get("/list", response_model=list[DepartmentResponse])
async def read_departments(db: Session = Depends(get_db)):
    return read_departments_service(db)

from sqlalchemy.orm import Session
from backend.api_departments.v1.models import Department
from backend.api_departments.v1.schemas import DepartmentCreate

def create_department_service(db, department_data):
    new_department = Department(name=department_data.name)
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department

def get_departments_service(db):
    return db.query(Department).all()
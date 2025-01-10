from fastapi import  FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from models import department, user
from settings.database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class UserBase(BaseModel):
    user_name: str = Field(min_length=3, x_length=50)  # Username, with a maximum length of 50
    first_name: str = Field(min_length=3 max_length=50)  # First name, with a maximum length of 50
    last_name: str = Field(min_length=3, max_length=50)   # Last name, with a maximum length of 50
    password: str = Field( min_length=8 max_length=50)  # Password (at least 6 characters)
    is_superuser: bool = Field(default=False)  # Default value for superuser flag
    is_reguser: bool = Field(default=True)      # Default value for regular user flag
    is_active: bool = Field(default=True)       # Default value for active status
    department: List[DepartmentBase]    # List of department

class DepartmentBase(BaseModel):
    department: str = Field(min_length=5, max_length=150) # Username, with a maximum length of 50
    is_deleted: bool = Field(default=False ) # Default value for deleted status

def get_db(self):
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends((get_db))]


@app.post("/user/")
async def create_user(user: UserBase, db: db_dependency):
    db_user = user.User(user_name=user.user_name,
                        first_name=user.first_name,
                        last_name=user.last_name,
                        password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    for
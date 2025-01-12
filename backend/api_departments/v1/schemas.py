from pydantic import BaseModel, Field
from typing import Optional
import uuid

class DepartmentBase(BaseModel):
    name: str = Field(min_length=3, max_length=150, description="The name of the department")
    description: Optional[str] = Field(None, max_length=250, description="A brief description of the department")
    is_deleted: Optional[bool] = Field(default=False, description="Whether the department is marked as deleted")

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    id: str

    class Config:
        from_attributes = True



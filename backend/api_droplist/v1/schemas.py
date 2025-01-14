# Schemas serialize and validate data. Below are the codes for defining Pydantic Schemas

from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import datetime

class DropListBase(BaseModel):
    name: str = Field(max_length=150, description="The name of the drop list")

class DropListCreate(DropListBase):
    created_by_id: Optional[UUID] = None
    updated_by_id: Optional[UUID] = None
    description: Optional[str] = None

class DropListUpdate(DropListBase):
    description: Optional[str] = None

class DropListResponse(DropListBase):
    description: Optional[str] = None
    created_by_id: Optional[UUID] = None
    updated_by_id: Optional[UUID] = None

    class Config:
        from_attributes = True

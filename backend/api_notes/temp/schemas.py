# Schemas serialize and validate data. Below are the codes for defining Pydantic Schemas

from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import datetime, date

class NotesBase(BaseModel):
    product_code: str = Field(max_length=80, description="The name of the department")
    lot_number: str = Field(None, max_length=80, description="A brief description of the department")
    product_kind_id: str = Field(None, max_length=10, description="A brief description of the department")
    stock_change_date: date

class NotesCreate(NotesBase):
    created_by_id: Optional[UUID] = None
    updated_by_id: Optional[UUID] = None

class NotesUpdate(NotesBase):
    pass

class NotesResponse(NotesBase):
    created_at: datetime
    created_by_id: Optional[UUID] = None
    updated_by_id: Optional[UUID] = None

    class Config:
        from_attributes = True

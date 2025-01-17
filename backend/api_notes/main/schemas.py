# Schemas serialize and validate data. Below are the codes for defining Pydantic Schemas

from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import datetime, date

class NotesBase(BaseModel):
    product_code: str = Field(max_length=80, description="The product code")
    lot_number: str = Field(None, max_length=80, description="The lot number")
    product_kind_id: str = Field(None, max_length=10, description="The product kind of the note")
    computed_detail_id: UUID
    stock_change_date: date

class NotesCreate(NotesBase):
    created_by_id: Optional[UUID] = None
    updated_by_id: Optional[UUID] = None


class NotesResponse(NotesBase):
    created_at: datetime
    created_by_id: Optional[UUID] = None
    updated_by_id: Optional[UUID] = None

    class Config:
        from_attributes = True

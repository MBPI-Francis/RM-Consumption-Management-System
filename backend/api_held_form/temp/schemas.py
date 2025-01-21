# Schemas serialize and validate data. Below are the codes for defining Pydantic Schemas

from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import date


class TempHeldForm(BaseModel):
    rm_code_id: UUID
    warehouse_id: UUID
    rm_soh_id: UUID
    current_status_id: UUID
    new_status_id: UUID
    change_status_date: date
    qty_kg: float


class TempHeldFormCreate(TempHeldForm):
    created_by_id: Optional[UUID] = None
    updated_by_id: Optional[UUID] = None

class TempHeldFormUpdate(TempHeldForm):
    pass

class TempHeldFormResponse(TempHeldForm):
    pass

    class Config:
        from_attributes = True

# Schemas serialize and validate data. Below are the codes for defining Pydantic Schemas

from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import datetime

class WarehouseBase(BaseModel):
    wh_number: int
    wh_name: str = Field(max_length=150, description="The name of the warehouse")

class WarehouseCreate(WarehouseBase):
    created_by_id: Optional[UUID] = None
    updated_by_id: Optional[UUID] = None
    description: Optional[str] = None

class WarehouseUpdate(WarehouseBase):
    pass
class WarehouseResponse(WarehouseBase):
    pass

    class Config:
        from_attributes = True

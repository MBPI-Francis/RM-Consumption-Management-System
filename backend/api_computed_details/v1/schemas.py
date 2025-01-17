# Schemas serialize and validate data. Below are the codes for defining Pydantic Schemas

from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import date

class ComputedDetailBase(BaseModel):
    computed_by_id: Optional[UUID] = None

class ComputedDetailCreate(ComputedDetailBase):
  pass

class ComputedDetailResponse(BaseModel):
    id: UUID
    computed_by_id: UUID
    date_computed: date

    class Config:
        from_attributes = True

# Schemas serialize and validate data. Below are the codes for defining Pydantic Schemas

from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import datetime

class StockOnHandBase(BaseModel):
    rm_code_id: UUID
    rm_soh : float


class StockOnHandCreate(StockOnHandBase):
    created_by_id: Optional[UUID] = None
    updated_by_id: Optional[UUID] = None
    description: Optional[str] = None
    
class StockOnHandUpdate(StockOnHandBase):
    rm_soh: Optional[str] = None
    description: Optional[str] = None


class StockOnHandResponse(StockOnHandBase):
    created_by_id: Optional[UUID] = None
    updated_by_id: Optional[UUID] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True

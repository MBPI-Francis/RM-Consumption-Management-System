# Schemas serialize and validate data. Below are the codes for defining Pydantic Schemas

from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import datetime

class RawMaterialBase(BaseModel):
    rm_code: str = Field(max_length=50, description="The code of the raw material")


class RawMaterialCreate(RawMaterialBase):
    created_by_id: Optional[UUID] = None
    updated_by_id: Optional[UUID] = None
    description: Optional[str] = None
    rm_name: Optional[str] = None

class RawMaterialUpdate(RawMaterialBase):
    rm_code: Optional[str]
    rm_name: Optional[str] = None
    description: Optional[str] = None


class RawMaterialResponse(RawMaterialBase):
    created_by_id: Optional[UUID] = None
    updated_by_id: Optional[UUID] = None
    description: Optional[str] = None
    rm_name: Optional[str] = None

    class Config:
        from_attributes = True

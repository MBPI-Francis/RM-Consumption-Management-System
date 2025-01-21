# Schemas serialize and validate data. Below are the codes for defining Pydantic Schemas

from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import date


class TransferForm(BaseModel):
    rm_code_id: UUID
    from_warehouse_id: UUID
    to_warehouse_id: UUID
    rm_soh_id: Optional[UUID] = None
    computed_detail_id: UUID
    status_id: Optional[UUID] = None
    ref_number: str = Field(max_length=50, description="The reference number of the Transfer Form")
    transfer_date: date
    qty_kg: float


class TransferFormCreate(TransferForm):
    created_by_id: Optional[UUID] = None
    updated_by_id: Optional[UUID] = None


class TransferFormResponse(TransferForm):
    pass

    class Config:
        from_attributes = True



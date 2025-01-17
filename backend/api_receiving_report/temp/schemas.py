# Schemas serialize and validate data. Below are the codes for defining Pydantic Schemas

from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import date


class TempReceivingReport(BaseModel):
    rm_code_id: UUID
    warehouse_id: UUID
    rm_soh_id: UUID
    ref_number: str = Field(max_length=50, description="The reference number of the Receiving Report")
    receiving_date: date
    qty_kg: float

class TempReceivingReportCreate(TempReceivingReport):
    created_by_id: Optional[UUID] = None
    updated_by_id: Optional[UUID] = None

class TempReceivingReportUpdate(TempReceivingReport):
    pass

class TempReceivingReportResponse(TempReceivingReport):
    pass

    class Config:
        from_attributes = True

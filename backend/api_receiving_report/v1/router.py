from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api_receiving_report.v1.schemas import ReceivingReportCreate, ReceivingReportUpdate, ReceivingReportResponse
from backend.api_receiving_report.v1.service import ReceivingReportService
from backend.settings.database import get_db
from uuid import UUID

router = APIRouter(prefix="/api/receiving_reports/v1")

@router.post("/create/", response_model=ReceivingReportResponse)
async def create_receiving_report(receiving_report: ReceivingReportCreate, db: get_db = Depends()):
    result = ReceivingReportService(db).create_receiving_report(receiving_report)
    return result

@router.get("/list/", response_model=list[ReceivingReportResponse])
async def read_receiving_report(db: get_db = Depends()):
    result = ReceivingReportService(db).get_receiving_report()
    return result

@router.put("/update/{receiving_report_id}/", response_model=ReceivingReportResponse)
async def update_receiving_report(receiving_report_id: UUID, receiving_report_update: ReceivingReportUpdate, db: get_db = Depends()):
    result = ReceivingReportService(db).update_receiving_report(receiving_report_id, receiving_report_update)
    return result

@router.put("/restore/{receiving_report_id}/", response_model=ReceivingReportResponse)
async def restore_receiving_report(receiving_report_id: UUID,  db: get_db = Depends()):
    result = ReceivingReportService(db).restore_receiving_report(receiving_report_id)
    return result

@router.delete("/delete/{receiving_report_id}/", response_model=ReceivingReportResponse)
async def delete_receiving_report(receiving_report_id: UUID, db: get_db = Depends()):
    result = ReceivingReportService(db).soft_delete_receiving_report(receiving_report_id)
    return result


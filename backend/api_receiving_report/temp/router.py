from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api_receiving_report.temp.schemas import TempReceivingReportCreate, TempReceivingReportUpdate, TempReceivingReportResponse, TempReceivingReport
from backend.api_receiving_report.temp.service import TempReceivingReportService
from backend.settings.database import get_db
from uuid import UUID

router = APIRouter(prefix="/api/receiving_reports/temp")

@router.post("/create/", response_model=TempReceivingReport)
async def create_receiving_report(receiving_report: TempReceivingReportCreate, db: get_db = Depends()):
    result = TempReceivingReportService(db).create_receiving_report(receiving_report)
    return result

@router.get("/list/", response_model=list[TempReceivingReportResponse])
async def read_receiving_report(db: get_db = Depends()):
    result = TempReceivingReportService(db).get_receiving_report()
    return result

@router.put("/update/{receiving_report_id}/", response_model=TempReceivingReportResponse)
async def update_receiving_report(receiving_report_id: UUID, receiving_report_update: TempReceivingReportUpdate, db: get_db = Depends()):
    result = TempReceivingReportService(db).update_receiving_report(receiving_report_id, receiving_report_update)
    return result

@router.put("/restore/{receiving_report_id}/", response_model=TempReceivingReportResponse)
async def restore_receiving_report(receiving_report_id: UUID,  db: get_db = Depends()):
    result = TempReceivingReportService(db).restore_receiving_report(receiving_report_id)
    return result

@router.delete("/delete/{receiving_report_id}/", response_model=TempReceivingReportResponse)
async def delete_receiving_report(receiving_report_id: UUID, db: get_db = Depends()):
    result = TempReceivingReportService(db).soft_delete_receiving_report(receiving_report_id)
    return result


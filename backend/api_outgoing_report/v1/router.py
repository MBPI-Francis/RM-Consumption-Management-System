from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api_outgoing_report.v1.schemas import OutgoingReportCreate, OutgoingReportUpdate, OutgoingReportResponse
from backend.api_outgoing_report.v1.service import OutgoingReportService
from backend.settings.database import get_db
from uuid import UUID

router = APIRouter(prefix="/api/outgoing_reports/temp")

@router.post("/create/", response_model=OutgoingReportResponse)
async def create_outgoing_report(outgoing_report: OutgoingReportCreate, db: get_db = Depends()):
    result = OutgoingReportService(db).create_outgoing_report(outgoing_report)
    return result

@router.get("/list/", response_model=list[OutgoingReportResponse])
async def read_outgoing_report(db: get_db = Depends()):
    result = OutgoingReportService(db).get_outgoing_report()
    return result

@router.put("/update/{outgoing_report_id}/", response_model=OutgoingReportResponse)
async def update_outgoing_report(outgoing_report_id: UUID, outgoing_report_update: OutgoingReportUpdate, db: get_db = Depends()):
    result = OutgoingReportService(db).update_outgoing_report(outgoing_report_id, outgoing_report_update)
    return result

@router.put("/restore/{outgoing_report_id}/", response_model=OutgoingReportResponse)
async def restore_outgoing_report(outgoing_report_id: UUID,  db: get_db = Depends()):
    result = OutgoingReportService(db).restore_outgoing_report(outgoing_report_id)
    return result

@router.delete("/delete/{outgoing_report_id}/", response_model=OutgoingReportResponse)
async def delete_outgoing_report(outgoing_report_id: UUID, db: get_db = Depends()):
    result = OutgoingReportService(db).soft_delete_outgoing_report(outgoing_report_id)
    return result


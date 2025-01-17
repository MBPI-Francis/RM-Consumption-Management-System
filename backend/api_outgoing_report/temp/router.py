from fastapi import APIRouter, Depends
from backend.api_outgoing_report.temp.schemas import TempOutgoingReportCreate, TempOutgoingReportUpdate, TempOutgoingReportResponse
from backend.api_outgoing_report.temp.service import TempOutgoingReportService
from backend.settings.database import get_db
from uuid import UUID

router = APIRouter(prefix="/api/outgoing_reports/temp")

@router.post("/create/", response_model=TempOutgoingReportResponse)
async def create_outgoing_report(outgoing_report: TempOutgoingReportCreate, db: get_db = Depends()):
    result = TempOutgoingReportService(db).create_outgoing_report(outgoing_report)
    return result

@router.get("/list/", response_model=list[TempOutgoingReportResponse])
async def read_outgoing_report(db: get_db = Depends()):
    result = TempOutgoingReportService(db).get_outgoing_report()
    return result

@router.put("/update/{outgoing_report_id}/", response_model=TempOutgoingReportResponse)
async def update_outgoing_report(outgoing_report_id: UUID, outgoing_report_update: TempOutgoingReportUpdate, db: get_db = Depends()):
    result = TempOutgoingReportService(db).update_outgoing_report(outgoing_report_id, outgoing_report_update)
    return result

@router.put("/restore/{outgoing_report_id}/", response_model=TempOutgoingReportResponse)
async def restore_outgoing_report(outgoing_report_id: UUID,  db: get_db = Depends()):
    result = TempOutgoingReportService(db).restore_outgoing_report(outgoing_report_id)
    return result

@router.delete("/delete/{outgoing_report_id}/", response_model=TempOutgoingReportResponse)
async def delete_outgoing_report(outgoing_report_id: UUID, db: get_db = Depends()):
    result = TempOutgoingReportService(db).soft_delete_outgoing_report(outgoing_report_id)
    return result


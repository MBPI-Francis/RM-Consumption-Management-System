from fastapi import APIRouter, Depends
from backend.api_receiving_report.main.schemas import ReceivingReportCreate, ReceivingReportResponse
from backend.api_receiving_report.main.service import ReceivingReportService
from backend.settings.database import get_db


router = APIRouter(prefix="/api/receiving_reports/main")

@router.post("/create/", response_model=ReceivingReportResponse)
async def create_receiving_report(receiving_report: ReceivingReportCreate, db: get_db = Depends()):
    result = ReceivingReportService(db).create_receiving_report(receiving_report)
    return result

@router.get("/list/", response_model=list[ReceivingReportResponse])
async def read_receiving_report(db: get_db = Depends()):
    result = ReceivingReportService(db).get_receiving_report()
    return result
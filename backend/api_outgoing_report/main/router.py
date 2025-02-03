from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api_outgoing_report.main.schemas import OutgoingReportCreate, OutgoingReportResponse
from backend.api_outgoing_report.main.service import (OutgoingReportService)
from backend.settings.database import get_db
from uuid import UUID

router = APIRouter(prefix="/api/outgoing_reports/main")

@router.post("/create/", response_model=OutgoingReportResponse)
async def create_outgoing_report(outgoing_report: OutgoingReportCreate, db: get_db = Depends()):
    result = OutgoingReportService(db).create_outgoing_report(outgoing_report)
    return result

@router.get("/list/", response_model=list[OutgoingReportResponse])
async def read_outgoing_report(db: get_db = Depends()):
    result = OutgoingReportService(db).get_outgoing_report()
    return result


import io
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..core.security import get_current_user, get_current_user_pdf
from ..models.user import User
from ..models.report import AnalysisReport
from ..schemas.report import ReportOut, ReportSummaryItem
from ..services.kpi_calculator import KPICalculator
from ..services.pdf_generator import PDFReportGenerator

router = APIRouter(prefix="/reports", tags=["Reports & Analytics"])

@router.get("", response_model=List[ReportSummaryItem])
def list_reports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    reports = db.query(AnalysisReport).order_by(AnalysisReport.created_at.desc()).all()
    return reports

@router.get("/{report_id}", response_model=ReportOut)
def get_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    report = db.query(AnalysisReport).filter(AnalysisReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Analysis report not found")
    return report

@router.get("/{report_id}/pdf")
def download_report_pdf(
    report_id: int,
    current_user: User = Depends(get_current_user_pdf),
    db: Session = Depends(get_db)
):
    report = db.query(AnalysisReport).filter(AnalysisReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Analysis report not found")
        
    calculator = KPICalculator(db)
    kpis = report.kpis_json or calculator.get_summary_kpis()
    cities = calculator.get_city_performance()
    
    report_dict = {
        "id": report.id,
        "title": report.title,
        "summary": report.summary,
        "verification_status": report.verification_status,
        "confidence_score": report.confidence_score,
        "verified_by": report.verified_by
    }
    
    buffer = io.BytesIO()
    PDFReportGenerator.generate_report_pdf(report_dict, kpis, cities, buffer)
    
    filename = f"Real_Estate_Decision_Intelligence_Report_{report.id}.pdf"
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

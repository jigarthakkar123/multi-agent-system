from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class ReportOut(BaseModel):
    id: int
    title: str
    industry: str
    period_start: str
    period_end: str
    summary: Optional[str] = None
    kpis_json: Optional[Dict[str, Any]] = None
    agent_insights_json: Optional[Dict[str, Any]] = None
    strategic_plan_json: Optional[Dict[str, Any]] = None
    verification_details_json: Optional[Dict[str, Any]] = None
    verification_status: str
    confidence_score: float
    verified_by: str
    execution_time_seconds: float
    created_at: datetime

    class Config:
        from_attributes = True

class ReportSummaryItem(BaseModel):
    id: int
    title: str
    industry: str
    created_at: datetime
    verification_status: str
    confidence_score: float

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ApprovalDecisionRequest(BaseModel):
    decision: str  # "Approved" or "Rejected"
    reason: Optional[str] = "Decision verified by executive management"

class HumanApprovalOut(BaseModel):
    id: int
    report_id: Optional[int] = None
    action_key: str
    title: str
    description: str
    category: str
    financial_impact: Optional[str] = None
    risk_level: str
    confidence_score: float
    status: str
    decision_reason: Optional[str] = None
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

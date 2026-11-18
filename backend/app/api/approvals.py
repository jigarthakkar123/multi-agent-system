from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.database import get_db
from ..core.security import get_current_user, require_role
from ..models.user import User
from ..models.approval import HumanApproval
from ..schemas.approval import HumanApprovalOut, ApprovalDecisionRequest

router = APIRouter(prefix="/approvals", tags=["Human-in-the-Loop Approvals"])

@router.get("", response_model=List[HumanApprovalOut])
def get_approvals(
    status: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(HumanApproval)
    if status:
        query = query.filter(HumanApproval.status == status)
    return query.order_by(HumanApproval.created_at.desc()).limit(limit).all()

@router.post("/{approval_id}/decision", response_model=HumanApprovalOut)
def record_approval_decision(
    approval_id: int,
    decision_in: ApprovalDecisionRequest,
    current_user: User = Depends(require_role(["admin", "manager"])),
    db: Session = Depends(get_db)
):
    """Authorized Business Manager or Admin reviews, approves, or rejects a consequential strategic action."""
    approval = db.query(HumanApproval).filter(HumanApproval.id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval request not found")
        
    if decision_in.decision not in ["Approved", "Rejected"]:
        raise HTTPException(status_code=400, detail="Decision must be 'Approved' or 'Rejected'")
        
    approval.status = decision_in.decision
    approval.decision_reason = decision_in.reason or f"Action {decision_in.decision.lower()} following multi-agent executive audit."
    approval.reviewed_by = f"{current_user.full_name} ({current_user.role.title()})"
    approval.reviewed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(approval)
    return approval

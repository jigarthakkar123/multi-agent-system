from fastapi import APIRouter, Depends, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.database import get_db
from ..core.security import require_role, get_current_user
from ..models.user import User
from ..models.audit_log import AgentExecutionLog
from ..models.report import AnalysisReport
from ..schemas.agents import AgentRunRequest, AgentStepLogOut, AgentStatusOut
from ..agents.crew_orchestrator import CrewOrchestrator

router = APIRouter(prefix="/agents", tags=["Multi-Agent Intelligence (CrewAI)"])

@router.post("/execute")
def execute_multi_agent_system(
    request: AgentRunRequest,
    current_user: User = Depends(require_role(["admin", "manager"])),
    db: Session = Depends(get_db)
):
    """Authorized Manager/Admin executes the 6 specialized AI agents sequentially or hierarchically."""
    orchestrator = CrewOrchestrator(db)
    result = orchestrator.run_multi_agent_pipeline(
        execution_mode=request.execution_mode,
        focus_city=request.focus_city
    )
    return result

@router.get("/status", response_model=List[AgentStatusOut])
def get_agents_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Returns the live operating status, active step transitions, and last thoughts of all 6 specialized agents."""
    agents = [
        {"name": "Data Analyst Agent", "role": "Senior Real Estate Data Analyst", "task": "Auditing 1,200 property listings, 600 deals, price/sqft trends, and absorption rates"},
        {"name": "Marketing Agent", "role": "Real Estate Growth & Acquisition Strategist", "task": "Auditing 1,800 leads across 6 channels, identifying Campaign and Referral conversion advantages"},
        {"name": "Finance Agent", "role": "Chief Financial Controller & Risk Analyst", "task": "Auditing Rs. 11.70 Cr commissions, Rs. 2.98 Cr expenses, and 74.58% net margin"},
        {"name": "Operations Agent", "role": "Head of Operations & Broker Network Efficiency", "task": "Evaluating 55 brokers and 1,200 site visits, optimizing second-visit conversion workflows"},
        {"name": "Strategy Agent", "role": "Chief Strategy Officer", "task": "Formulating 90-day turnaround plan and staging consequential Human Approval initiatives"},
        {"name": "Verification Agent", "role": "Chief Quality & Compliance Verification Auditor", "task": "Cross-verifying all numerical claims against ground truth; calculating empirical confidence score and verification statement"}
    ]
    
    results = []
    for a in agents:
        last_log = (
            db.query(AgentExecutionLog)
            .filter(AgentExecutionLog.agent_name == a["name"])
            .order_by(AgentExecutionLog.created_at.desc())
            .first()
        )
        status = "Completed" if last_log else "Idle"
        last_thought = last_log.log_message[:240] + ("..." if len(last_log.log_message) > 240 else "") if last_log else "Standing by for execution trigger."
        
        results.append({
            "agent_name": a["name"],
            "role": a["role"],
            "status": status,
            "current_task": a["task"],
            "completed_steps": 1 if last_log else 0,
            "total_steps": 1,
            "last_thought": last_thought
        })
    return results

@router.get("/logs", response_model=List[AgentStepLogOut])
def get_agent_logs(
    run_id: Optional[str] = None,
    agent_name: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves step-by-step logs for agent monitoring."""
    query = db.query(AgentExecutionLog)
    if run_id:
        query = query.filter(AgentExecutionLog.run_id == run_id)
    if agent_name:
        query = query.filter(AgentExecutionLog.agent_name == agent_name)
    return query.order_by(AgentExecutionLog.created_at.desc()).limit(limit).all()

@router.get("/runs")
def get_previous_runs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Returns previous analysis runs with report IDs."""
    reports = db.query(AnalysisReport).order_by(AnalysisReport.created_at.desc()).limit(20).all()
    return [
        {
            "report_id": r.id,
            "title": r.title,
            "created_at": r.created_at,
            "verification_status": r.verification_status,
            "confidence_score": r.confidence_score,
            "execution_time_seconds": r.execution_time_seconds,
            "engine_used": (r.verification_details_json or {}).get("engine_used")
        }
        for r in reports
    ]

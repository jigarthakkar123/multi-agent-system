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

@router.get("/diagnostic")
def get_engine_diagnostic(
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Admin-only diagnostic endpoint to inspect live environment, CrewAI installation, and LLM configuration."""
    import os, sys
    from ..agents.crewai_engine import HAS_CREWAI_PKG, CREWAI_IMPORT_ERROR, LAST_CREWAI_ERROR
    from ..core.config import settings

    diag = {
        "python_version": sys.version,
        "has_crewai_pkg": HAS_CREWAI_PKG,
        "crewai_import_error": CREWAI_IMPORT_ERROR,
        "last_crewai_error": LAST_CREWAI_ERROR,
        "openai_key_configured": bool(os.getenv("OPENAI_API_KEY") or settings.OPENAI_API_KEY),
        "gemini_key_configured": bool(os.getenv("GEMINI_API_KEY") or settings.GEMINI_API_KEY),
    }

    if HAS_CREWAI_PKG:
        try:
            import crewai
            diag["crewai_version"] = getattr(crewai, "__version__", "unknown")
            from crewai import Agent as TestAgent, Task as TestTask, Crew as TestCrew
            from ..agents.custom_tools import get_core_kpis_tool
            diag["tool_type"] = str(type(get_core_kpis_tool))
            chosen_llm = "gemini/gemini-2.5-flash" if diag["gemini_key_configured"] else ("gpt-4o-mini" if diag["openai_key_configured"] else None)
            diag["chosen_llm"] = chosen_llm
            if diag["gemini_key_configured"]:
                g_k = os.getenv("GEMINI_API_KEY") or settings.GEMINI_API_KEY
                os.environ["GOOGLE_API_KEY"] = g_k
                os.environ["GEMINI_API_KEY"] = g_k

            test_llm = chosen_llm
            try:
                from crewai import LLM as CrewLLM
                test_llm = CrewLLM(model=chosen_llm, api_key=os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY"))
            except Exception:
                test_llm = chosen_llm

            test_agent = TestAgent(
                role="Test Analyst",
                goal="Testing instantiation",
                backstory="Test backstory",
                tools=[get_core_kpis_tool],
                llm=test_llm,
                verbose=False
            )
            diag["agent_instantiation"] = "SUCCESS"
        except Exception as e:
            diag["agent_instantiation"] = f"ERROR: {type(e).__name__}: {str(e)}"
    else:
        diag["agent_instantiation"] = "CREWAI_PKG_NOT_INSTALLED"

    # Test direct connectivity to LLMs without exposing sensitive keys
    if diag["gemini_key_configured"]:
        try:
            import httpx
            g_key = os.getenv("GEMINI_API_KEY") or settings.GEMINI_API_KEY
            # List available models for this key
            try:
                list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={g_key}"
                l_res = httpx.get(list_url, timeout=5.0)
                if l_res.status_code == 200:
                    diag["gemini_models_available"] = [m.get("name") for m in l_res.json().get("models", [])[:8]]
                else:
                    diag["gemini_list_models_status"] = f"HTTP {l_res.status_code}: {l_res.text[:200]}"
            except Exception as le:
                diag["gemini_list_models_status"] = f"ERROR: {le}"

            g_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={g_key}"
            g_res = httpx.post(g_url, json={"contents": [{"parts": [{"text": "Say OK"}]}]}, timeout=5.0)
            diag["gemini_direct_status"] = f"HTTP {g_res.status_code}"
            if g_res.status_code != 200:
                diag["gemini_error_body"] = g_res.text[:200]
        except Exception as e:
            diag["gemini_direct_status"] = f"ERROR: {e}"

    if diag["openai_key_configured"]:
        try:
            import httpx
            o_key = os.getenv("OPENAI_API_KEY") or settings.OPENAI_API_KEY
            o_res = httpx.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {o_key}"},
                json={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": "Say OK"}]},
                timeout=5.0
            )
            diag["openai_direct_status"] = f"HTTP {o_res.status_code}"
        except Exception as e:
            diag["openai_direct_status"] = f"ERROR: {e}"

    return diag

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

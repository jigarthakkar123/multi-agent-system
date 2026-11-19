from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class AgentRunRequest(BaseModel):
    execution_mode: str = "sequential"  # "sequential" or "hierarchical"
    focus_city: Optional[str] = None
    focus_property_type: Optional[str] = None
    custom_instructions: Optional[str] = None
    api_key: Optional[str] = None
    llm_provider: Optional[str] = None

class AgentStepLogOut(BaseModel):
    id: int
    run_id: str
    agent_name: str
    agent_role: Optional[str] = None
    step_name: str
    status: str
    log_message: str
    created_at: datetime

    class Config:
        from_attributes = True

class AgentStatusOut(BaseModel):
    agent_name: str
    role: str
    status: str  # Idle, Working, Completed, Verified, Failed
    current_task: Optional[str] = None
    completed_steps: int = 0
    total_steps: int = 1
    last_thought: Optional[str] = None

class MultiAgentRunSummary(BaseModel):
    run_id: str
    execution_mode: str
    status: str
    agents_status: List[AgentStatusOut]
    report_id: Optional[int] = None
    created_at: datetime

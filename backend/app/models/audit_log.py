from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from ..core.database import Base

class AgentExecutionLog(Base):
    __tablename__ = "agent_execution_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(String(100), index=True, nullable=False)
    report_id = Column(Integer, ForeignKey("analysis_reports.id"), nullable=True)
    
    agent_name = Column(String(100), index=True, nullable=False) # Data Analyst, Marketing, Finance, Operations, Strategy, Verification
    agent_role = Column(String(150), nullable=True)
    step_name = Column(String(150), nullable=False)
    status = Column(String(50), default="Completed") # Started, In Progress, Completed, Failed, Warning
    
    log_message = Column(Text, nullable=False)
    metrics_snapshot = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    report = relationship("AnalysisReport", back_populates="execution_logs")

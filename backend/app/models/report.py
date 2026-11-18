from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.orm import relationship
from ..core.database import Base

class AnalysisReport(Base):
    __tablename__ = "analysis_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    industry = Column(String(100), default="Real Estate")
    period_start = Column(String(20), default="2026-05-01")
    period_end = Column(String(20), default="2026-10-31")
    summary = Column(Text, nullable=True)
    
    # JSON breakdown
    kpis_json = Column(JSON, nullable=True)
    agent_insights_json = Column(JSON, nullable=True)
    strategic_plan_json = Column(JSON, nullable=True)
    verification_details_json = Column(JSON, nullable=True)
    
    verification_status = Column(String(50), default="Pending") # Verified & Approved, Flagged, Rejected
    confidence_score = Column(Float, default=95.0)
    verified_by = Column(String(100), default="Verification Agent (Automated + Auditor)")
    execution_time_seconds = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    approvals = relationship("HumanApproval", back_populates="report", cascade="all, delete-orphan")
    execution_logs = relationship("AgentExecutionLog", back_populates="report", cascade="all, delete-orphan")

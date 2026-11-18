from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base

class HumanApproval(Base):
    __tablename__ = "human_approvals"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("analysis_reports.id"), nullable=True)
    
    action_key = Column(String(100), index=True) # e.g. "REALLOCATE_MARKETING_BUDGET"
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), default="Marketing & Growth") # Marketing, Pricing, Operations, Commission, Expansion
    
    financial_impact = Column(String(100), nullable=True) # e.g. "+₹45,00,000 / -₹12,00,000"
    risk_level = Column(String(50), default="Medium")      # Low, Medium, High, Critical
    confidence_score = Column(Float, default=92.5)
    
    status = Column(String(50), default="Pending")         # Pending, Approved, Rejected
    decision_reason = Column(Text, nullable=True)
    reviewed_by = Column(String(150), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    report = relationship("AnalysisReport", back_populates="approvals")

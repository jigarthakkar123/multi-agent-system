from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base

class BusinessProfile(Base):
    __tablename__ = "business_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    company_name = Column(String(255), default="Apex Realty Intelligence Corp")
    industry = Column(String(100), default="Real Estate - Property & Sales Intelligence")
    team_size = Column(Integer, default=55)
    business_goals = Column(Text, default="Optimize sales agent conversion velocity, minimize marketing spend leakage, accelerate listing absorption in Western India property hubs, and ensure zero-hallucination executive decision intelligence.")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="profile")

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BusinessProfileBase(BaseModel):
    company_name: str = "Apex Realty Intelligence Corp"
    industry: str = "Real Estate - Property & Sales Intelligence"
    team_size: int = 55
    business_goals: str = "Optimize sales agent conversion velocity, minimize marketing spend leakage, accelerate listing absorption in Western India property hubs, and ensure zero-hallucination executive decision intelligence."

class BusinessProfileUpdate(BusinessProfileBase):
    pass

class BusinessProfileOut(BusinessProfileBase):
    id: int
    user_id: Optional[int] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

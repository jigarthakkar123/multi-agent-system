from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class PropertyOut(BaseModel):
    property_id: str
    property_type: str
    city: str
    locality: str
    bedrooms: int
    area_sqft: float
    asking_price: float
    listing_date: date
    listing_status: str

    class Config:
        from_attributes = True

class LeadOut(BaseModel):
    lead_id: str
    lead_name: str
    property_type_interest: str
    city: str
    lead_source: str
    inquiry_date: date
    budget_min: float
    budget_max: float
    lead_status: str
    phone: Optional[str] = None

    class Config:
        from_attributes = True

class SiteVisitOut(BaseModel):
    visit_id: str
    lead_id: str
    property_id: str
    visit_date: date
    visit_feedback: str
    visit_outcome: str
    agent_id: str

    class Config:
        from_attributes = True

class DealOut(BaseModel):
    deal_id: str
    lead_id: str
    property_id: str
    deal_date: date
    deal_status: str
    sale_price: float
    commission_rate: float
    agent_id: str

    class Config:
        from_attributes = True

class ExpenseOut(BaseModel):
    expense_id: str
    expense_date: date
    project_id: str
    category: str
    amount: float
    vendor: Optional[str] = None

    class Config:
        from_attributes = True

class DatasetSummaryOut(BaseModel):
    total_properties: int
    total_leads: int
    total_visits: int
    total_deals: int
    total_agent_records: int
    total_expenses: int
    date_coverage: str
    cities: List[str]
    property_types: List[str]
    total_inventory_value: float
    total_closed_sales_volume: float
    total_expenses_amount: float

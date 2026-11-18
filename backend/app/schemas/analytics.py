from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class KPIOverviewOut(BaseModel):
    total_revenue: float
    total_commission: float
    total_expenses: float
    net_profit: float
    profit_margin_pct: float
    total_leads: int
    converted_leads: int
    conversion_rate_pct: float
    total_deals: int
    closed_won_deals: int
    deal_win_rate_pct: float
    total_inventory_units: int
    sold_inventory_units: int
    absorption_rate_pct: float
    avg_property_price_sqft: float
    avg_deal_size: float
    cost_per_acquisition: float

class MonthlyTrendItem(BaseModel):
    month: str
    revenue: float
    commission: float
    expenses: float
    profit: float
    deals_closed: int
    leads_count: int

class CityPerformanceItem(BaseModel):
    city: str
    property_count: int
    total_inventory_value: float
    avg_price: float
    deals_closed: int
    revenue_generated: float
    leads_count: int
    conversion_rate: float

class PropertyTypeDistributionItem(BaseModel):
    property_type: str
    count: int
    total_value: float
    avg_price: float
    sold_count: int

class LeadFunnelItem(BaseModel):
    stage: str
    count: int
    percentage: float

class LeadSourceItem(BaseModel):
    source: str
    total_leads: int
    converted: int
    conversion_rate: float

class AgentLeaderboardItem(BaseModel):
    agent_id: str
    total_calls: int
    total_visits: int
    deals_closed: int
    total_sales_value: float
    total_commission_earned: float
    avg_customer_rating: float
    total_marketing_spend: float
    roi_multiple: float

class CategoryExpenseItem(BaseModel):
    category: str
    amount: float
    percentage: float

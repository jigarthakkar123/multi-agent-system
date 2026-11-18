from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..services.kpi_calculator import KPICalculator
from ..schemas.analytics import (
    KPIOverviewOut, MonthlyTrendItem, CityPerformanceItem,
    PropertyTypeDistributionItem, LeadFunnelItem, LeadSourceItem,
    AgentLeaderboardItem, CategoryExpenseItem
)

router = APIRouter(prefix="/analytics", tags=["Analytics & Business Intelligence"])

@router.get("/kpis", response_model=KPIOverviewOut)
def get_kpis(db: Session = Depends(get_db)):
    calculator = KPICalculator(db)
    return calculator.get_summary_kpis()

@router.get("/monthly-trends", response_model=List[MonthlyTrendItem])
def get_monthly_trends(db: Session = Depends(get_db)):
    calculator = KPICalculator(db)
    return calculator.get_monthly_trends()

@router.get("/city-performance", response_model=List[CityPerformanceItem])
def get_city_performance(db: Session = Depends(get_db)):
    calculator = KPICalculator(db)
    return calculator.get_city_performance()

@router.get("/property-types", response_model=List[PropertyTypeDistributionItem])
def get_property_types(db: Session = Depends(get_db)):
    calculator = KPICalculator(db)
    return calculator.get_property_type_distribution()

@router.get("/lead-funnel", response_model=List[LeadFunnelItem])
def get_lead_funnel(db: Session = Depends(get_db)):
    calculator = KPICalculator(db)
    return calculator.get_lead_funnel()

@router.get("/lead-sources", response_model=List[LeadSourceItem])
def get_lead_sources(db: Session = Depends(get_db)):
    calculator = KPICalculator(db)
    return calculator.get_lead_sources()

@router.get("/agent-leaderboard", response_model=List[AgentLeaderboardItem])
def get_agent_leaderboard(
    limit: int = Query(15, ge=1, le=55),
    db: Session = Depends(get_db)
):
    calculator = KPICalculator(db)
    return calculator.get_agent_leaderboard(limit=limit)

@router.get("/expense-breakdown", response_model=List[CategoryExpenseItem])
def get_expense_breakdown(db: Session = Depends(get_db)):
    calculator = KPICalculator(db)
    return calculator.get_category_expenses()

import json
from sqlalchemy.orm import Session
from ..services.kpi_calculator import KPICalculator

class RealEstateAnalyticsTools:
    """Deterministic analytics tools providing ground-truth data to agents."""
    
    def __init__(self, db: Session):
        self.calculator = KPICalculator(db)
        
    def get_core_kpis(self) -> str:
        """Returns the core calculated real estate business KPIs."""
        kpis = self.calculator.get_summary_kpis()
        return json.dumps(kpis, indent=2)

    def get_monthly_financial_trends(self) -> str:
        """Returns monthly revenue, brokerage commission, and operational expenses (May-Oct 2026)."""
        trends = self.calculator.get_monthly_trends()
        return json.dumps(trends, indent=2)

    def get_city_market_data(self) -> str:
        """Returns property inventory, deals closed, and revenue generated across cities."""
        city_perf = self.calculator.get_city_performance()
        return json.dumps(city_perf, indent=2)

    def get_lead_acquisition_and_funnel(self) -> str:
        """Returns lead source breakdown and funnel conversion rates."""
        funnel = self.calculator.get_lead_funnel()
        sources = self.calculator.get_lead_sources()
        return json.dumps({"funnel_stages": funnel, "lead_sources": sources}, indent=2)

    def get_agent_operational_productivity(self) -> str:
        """Returns top agent productivity metrics (calls, site visits, deals, commission, customer rating)."""
        leaderboard = self.calculator.get_agent_leaderboard(limit=15)
        return json.dumps(leaderboard, indent=2)

    def get_expense_breakdown(self) -> str:
        """Returns operational expenses grouped by category (Legal, Brokerage, Rent, Maintenance, etc.)."""
        expenses = self.calculator.get_category_expenses()
        return json.dumps(expenses, indent=2)

    def get_property_type_absorption(self) -> str:
        """Returns inventory units, average pricing, and sold units by property type."""
        props = self.calculator.get_property_type_distribution()
        return json.dumps(props, indent=2)

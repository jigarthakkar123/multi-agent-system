import json
from sqlalchemy.orm import Session
from ..core.database import SessionLocal
from ..services.kpi_calculator import KPICalculator

# -------------------------------------------------------------------------
# CrewAI / LangChain @tool Decorator Integration
# -------------------------------------------------------------------------
try:
    from crewai.tools import tool
except ImportError:
    try:
        from langchain.tools import tool
    except ImportError:
        def tool(name_or_func=None, **kwargs):
            if callable(name_or_func):
                return name_or_func
            def decorator(func):
                return func
            return decorator

@tool("get_core_kpis")
def get_core_kpis_tool() -> str:
    """Returns core real estate business KPIs (Revenue, Commission, Expenses, Margin) from database."""
    db = SessionLocal()
    try:
        calc = KPICalculator(db)
        return json.dumps(calc.get_summary_kpis(), indent=2)
    finally:
        db.close()

@tool("get_city_market_data")
def get_city_market_data_tool() -> str:
    """Returns property inventory, deals closed, and revenue generated across metropolitan hubs."""
    db = SessionLocal()
    try:
        calc = KPICalculator(db)
        return json.dumps(calc.get_city_performance(), indent=2)
    finally:
        db.close()

@tool("get_lead_acquisition_and_funnel")
def get_lead_acquisition_and_funnel_tool() -> str:
    """Returns lead acquisition channel conversion hierarchy, inquiry volumes, and funnel stages."""
    db = SessionLocal()
    try:
        calc = KPICalculator(db)
        return json.dumps({"funnel_stages": calc.get_lead_funnel(), "lead_sources": calc.get_lead_sources()}, indent=2)
    finally:
        db.close()

@tool("get_expense_breakdown")
def get_expense_breakdown_tool() -> str:
    """Returns operational expenses grouped by category (Advertising, Maintenance, Legal, etc.)."""
    db = SessionLocal()
    try:
        calc = KPICalculator(db)
        return json.dumps(calc.get_category_expenses(), indent=2)
    finally:
        db.close()

@tool("get_agent_operational_productivity")
def get_agent_operational_productivity_tool() -> str:
    """Returns broker productivity metrics (deals closed, commission earned, customer rating)."""
    db = SessionLocal()
    try:
        calc = KPICalculator(db)
        return json.dumps(calc.get_agent_leaderboard(limit=15), indent=2)
    finally:
        db.close()

@tool("get_site_visit_analytics")
def get_site_visit_analytics_tool() -> str:
    """Returns physical site visit outcomes, second visit requests, and buyer offer expectations."""
    db = SessionLocal()
    try:
        calc = KPICalculator(db)
        return json.dumps(calc.get_site_visit_analytics(), indent=2)
    finally:
        db.close()

@tool("get_property_type_absorption")
def get_property_type_absorption_tool() -> str:
    """Returns inventory units, average pricing, and sold units by property type."""
    db = SessionLocal()
    try:
        calc = KPICalculator(db)
        return json.dumps(calc.get_property_type_distribution(), indent=2)
    finally:
        db.close()

@tool("get_broker_concentration")
def get_broker_concentration_tool() -> str:
    """Returns top broker concentration metrics, commission percentages, and top broker IDs."""
    db = SessionLocal()
    try:
        calc = KPICalculator(db)
        return json.dumps(calc.get_broker_concentration(), indent=2)
    finally:
        db.close()

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

    def get_site_visit_analytics(self) -> str:
        """Returns empirical site visit outcomes (Offer Expected, Second Visit, etc.) and customer feedbacks."""
        analytics = self.calculator.get_site_visit_analytics()
        return json.dumps(analytics, indent=2)

    def get_broker_concentration(self) -> str:
        """Returns top broker concentration metrics, commission percentages, and top broker IDs."""
        conc = self.calculator.get_broker_concentration()
        return json.dumps(conc, indent=2)

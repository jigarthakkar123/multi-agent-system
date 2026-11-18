import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.real_estate import Property, Lead, SiteVisit, Deal, AgentPerformance, Expense

class KPICalculator:
    def __init__(self, db: Session):
        self.db = db

    def get_summary_kpis(self) -> dict:
        """Calculates core business KPIs strictly from database records."""
        # Closed Won Deals
        closed_deals = self.db.query(Deal).filter(Deal.deal_status == "Closed Won").all()
        total_revenue = sum([d.sale_price for d in closed_deals]) if closed_deals else 0.0
        total_commission = sum([d.sale_price * d.commission_rate for d in closed_deals]) if closed_deals else 0.0
        
        # Expenses
        expenses = self.db.query(Expense).all()
        total_expenses = sum([e.amount for e in expenses]) if expenses else 0.0
        
        # Net Profit & Margin
        net_profit = total_commission - total_expenses
        profit_margin_pct = (net_profit / total_commission * 100) if total_commission > 0 else 0.0
        
        # Leads Funnel
        total_leads = self.db.query(Lead).count()
        converted_leads = self.db.query(Lead).filter(Lead.lead_status == "Converted").count()
        conversion_rate_pct = (converted_leads / total_leads * 100) if total_leads > 0 else 0.0
        
        # Deals
        total_deals_count = self.db.query(Deal).count()
        closed_won_count = len(closed_deals)
        deal_win_rate_pct = (closed_won_count / total_deals_count * 100) if total_deals_count > 0 else 0.0
        
        # Inventory Absorption
        total_inventory_units = self.db.query(Property).count()
        sold_inventory_units = self.db.query(Property).filter(Property.listing_status == "Sold").count()
        absorption_rate_pct = (sold_inventory_units / total_inventory_units * 100) if total_inventory_units > 0 else 0.0
        
        # Average Price per SqFt across all properties
        properties = self.db.query(Property).all()
        valid_props = [p for p in properties if p.area_sqft > 0]
        avg_price_sqft = (sum([p.asking_price / p.area_sqft for p in valid_props]) / len(valid_props)) if valid_props else 0.0
        
        avg_deal_size = (total_revenue / closed_won_count) if closed_won_count > 0 else 0.0
        cost_per_acquisition = (total_expenses / converted_leads) if converted_leads > 0 else 0.0
        
        return {
            "total_revenue": round(total_revenue, 2),
            "total_commission": round(total_commission, 2),
            "total_expenses": round(total_expenses, 2),
            "net_profit": round(net_profit, 2),
            "profit_margin_pct": round(profit_margin_pct, 2),
            "total_leads": total_leads,
            "converted_leads": converted_leads,
            "conversion_rate_pct": round(conversion_rate_pct, 2),
            "total_deals": total_deals_count,
            "closed_won_deals": closed_won_count,
            "deal_win_rate_pct": round(deal_win_rate_pct, 2),
            "total_inventory_units": total_inventory_units,
            "sold_inventory_units": sold_inventory_units,
            "absorption_rate_pct": round(absorption_rate_pct, 2),
            "avg_property_price_sqft": round(avg_price_sqft, 2),
            "avg_deal_size": round(avg_deal_size, 2),
            "cost_per_acquisition": round(cost_per_acquisition, 2)
        }

    def get_monthly_trends(self) -> list:
        """Returns monthly trends for revenue, expenses, and deals (May-Oct 2026)."""
        deals = self.db.query(Deal).all()
        expenses = self.db.query(Expense).all()
        leads = self.db.query(Lead).all()
        
        months = ["2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10"]
        monthly_map = {m: {"revenue": 0.0, "commission": 0.0, "expenses": 0.0, "deals_closed": 0, "leads_count": 0} for m in months}
        
        for d in deals:
            m = d.deal_date.strftime("%Y-%m")
            if m in monthly_map and d.deal_status == "Closed Won":
                monthly_map[m]["revenue"] += d.sale_price
                monthly_map[m]["commission"] += (d.sale_price * d.commission_rate)
                monthly_map[m]["deals_closed"] += 1
                
        for e in expenses:
            m = e.expense_date.strftime("%Y-%m")
            if m in monthly_map:
                monthly_map[m]["expenses"] += e.amount
                
        for l in leads:
            m = l.inquiry_date.strftime("%Y-%m")
            if m in monthly_map:
                monthly_map[m]["leads_count"] += 1
                
        result = []
        for m in sorted(monthly_map.keys()):
            item = monthly_map[m]
            profit = item["commission"] - item["expenses"]
            result.append({
                "month": m,
                "revenue": round(item["revenue"], 2),
                "commission": round(item["commission"], 2),
                "expenses": round(item["expenses"], 2),
                "profit": round(profit, 2),
                "deals_closed": item["deals_closed"],
                "leads_count": item["leads_count"]
            })
        return result

    def get_city_performance(self) -> list:
        """Calculates performance aggregated by city."""
        cities = ["Mumbai", "Pune", "Ahmedabad", "Surat", "Vadodara", "Rajkot", "Anand", "Bharuch", "Gandhinagar", "Nadiad"]
        results = []
        
        for city in cities:
            props = self.db.query(Property).filter(Property.city == city).all()
            leads = self.db.query(Lead).filter(Lead.city == city).all()
            
            prop_ids = [p.property_id for p in props]
            deals = self.db.query(Deal).filter(Deal.property_id.in_(prop_ids), Deal.deal_status == "Closed Won").all() if prop_ids else []
            
            prop_count = len(props)
            inv_val = sum([p.asking_price for p in props]) if props else 0.0
            avg_price = (inv_val / prop_count) if prop_count > 0 else 0.0
            
            closed_count = len(deals)
            revenue = sum([d.sale_price for d in deals]) if deals else 0.0
            
            lead_count = len(leads)
            conv_leads = len([l for l in leads if l.lead_status == "Converted"])
            conv_rate = (conv_leads / lead_count * 100) if lead_count > 0 else 0.0
            
            results.append({
                "city": city,
                "property_count": prop_count,
                "total_inventory_value": round(inv_val, 2),
                "avg_price": round(avg_price, 2),
                "deals_closed": closed_count,
                "revenue_generated": round(revenue, 2),
                "leads_count": lead_count,
                "conversion_rate": round(conv_rate, 2)
            })
            
        return sorted(results, key=lambda x: x["revenue_generated"], reverse=True)

    def get_property_type_distribution(self) -> list:
        """Distribution by property type (Villa, Apartment, Office, Plot, Warehouse, Shop)."""
        prop_types = ["Villa", "Apartment", "Office", "Plot", "Warehouse", "Shop"]
        results = []
        
        for pt in prop_types:
            props = self.db.query(Property).filter(Property.property_type == pt).all()
            count = len(props)
            tot_val = sum([p.asking_price for p in props]) if props else 0.0
            avg_pr = (tot_val / count) if count > 0 else 0.0
            sold = len([p for p in props if p.listing_status == "Sold"])
            
            results.append({
                "property_type": pt,
                "count": count,
                "total_value": round(tot_val, 2),
                "avg_price": round(avg_pr, 2),
                "sold_count": sold
            })
        return results

    def get_lead_funnel(self) -> list:
        """Lead funnel conversion breakdown."""
        total = self.db.query(Lead).count()
        stages = ["New", "Qualified", "Negotiation", "Converted", "Lost"]
        results = []
        for s in stages:
            c = self.db.query(Lead).filter(Lead.lead_status == s).count()
            pct = (c / total * 100) if total > 0 else 0.0
            results.append({
                "stage": s,
                "count": c,
                "percentage": round(pct, 2)
            })
        return results

    def get_lead_sources(self) -> list:
        """Performance by lead source."""
        sources = ["Walk-in", "Website", "Social Media", "Referral", "Campaign", "Portal"]
        results = []
        for src in sources:
            leads = self.db.query(Lead).filter(Lead.lead_source == src).all()
            tot = len(leads)
            conv = len([l for l in leads if l.lead_status == "Converted"])
            rate = (conv / tot * 100) if tot > 0 else 0.0
            results.append({
                "source": src,
                "total_leads": tot,
                "converted": conv,
                "conversion_rate": round(rate, 2)
            })
        return sorted(results, key=lambda x: x["conversion_rate"], reverse=True)

    def get_category_expenses(self) -> list:
        """Expense breakdown by category."""
        expenses = self.db.query(Expense).all()
        tot = sum([e.amount for e in expenses]) if expenses else 0.0
        cats = {}
        for e in expenses:
            cats[e.category] = cats.get(e.category, 0.0) + e.amount
            
        results = []
        for cat, amt in cats.items():
            pct = (amt / tot * 100) if tot > 0 else 0.0
            results.append({
                "category": cat,
                "amount": round(amt, 2),
                "percentage": round(pct, 2)
            })
        return sorted(results, key=lambda x: x["amount"], reverse=True)

    def get_agent_leaderboard(self, limit: int = 15) -> list:
        """Top real estate agents by deals, commission, and ROI."""
        deals = self.db.query(Deal).filter(Deal.deal_status == "Closed Won").all()
        perfs = self.db.query(AgentPerformance).all()
        
        agent_data = {}
        for p in perfs:
            aid = p.agent_id
            if aid not in agent_data:
                agent_data[aid] = {
                    "agent_id": aid,
                    "total_calls": 0,
                    "total_visits": 0,
                    "deals_closed": 0,
                    "total_sales_value": 0.0,
                    "total_commission_earned": 0.0,
                    "ratings": [],
                    "total_marketing_spend": 0.0
                }
            agent_data[aid]["total_calls"] += p.calls_made
            agent_data[aid]["total_visits"] += p.visits_conducted
            agent_data[aid]["deals_closed"] += p.deals_closed
            agent_data[aid]["ratings"].append(p.customer_rating)
            agent_data[aid]["total_marketing_spend"] += p.marketing_spend
            
        for d in deals:
            aid = d.agent_id
            if aid in agent_data:
                agent_data[aid]["total_sales_value"] += d.sale_price
                agent_data[aid]["total_commission_earned"] += (d.sale_price * d.commission_rate)
                
        results = []
        for aid, data in agent_data.items():
            avg_rating = sum(data["ratings"]) / len(data["ratings"]) if data["ratings"] else 0.0
            spend = data["total_marketing_spend"]
            comm = data["total_commission_earned"]
            roi = (comm / spend) if spend > 0 else 0.0
            results.append({
                "agent_id": aid,
                "total_calls": data["total_calls"],
                "total_visits": data["total_visits"],
                "deals_closed": data["deals_closed"],
                "total_sales_value": round(data["total_sales_value"], 2),
                "total_commission_earned": round(comm, 2),
                "avg_customer_rating": round(avg_rating, 2),
                "total_marketing_spend": round(spend, 2),
                "roi_multiple": round(roi, 2)
            })
            
        return sorted(results, key=lambda x: x["total_commission_earned"], reverse=True)[:limit]

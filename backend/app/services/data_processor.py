import os
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from ..models.real_estate import Property, Lead, SiteVisit, Deal, AgentPerformance, Expense
from ..core.database import SessionLocal

class DataProcessor:
    @staticmethod
    def load_and_clean_excel(file_path: str):
        """Loads and cleans the 6 real estate sheets from an Excel file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset file not found at: {file_path}")
            
        excel_file = pd.ExcelFile(file_path)
        sheet_names = excel_file.sheet_names
        
        # Mapping sheet names case-insensitively
        name_map = {}
        for s in sheet_names:
            clean = s.strip().lower()
            name_map[clean] = s
            
        properties_df = excel_file.parse(name_map.get("properties", "Properties"))
        leads_df = excel_file.parse(name_map.get("leads", "Leads"))
        
        visits_sheet = name_map.get("site_visits", name_map.get("visits", "Site_Visits"))
        visits_df = excel_file.parse(visits_sheet)
        
        deals_df = excel_file.parse(name_map.get("deals", "Deals"))
        
        perf_sheet = name_map.get("agent_performance", name_map.get("performance", "Agent_Performance"))
        perf_df = excel_file.parse(perf_sheet)
        
        expenses_df = excel_file.parse(name_map.get("expenses", "Expenses"))
        
        # Clean, validate, deduplicate and standardize Properties
        properties_df["property_id"] = properties_df["property_id"].astype(str).str.strip()
        properties_df = properties_df.drop_duplicates(subset=["property_id"])
        properties_df["property_type"] = properties_df["property_type"].astype(str).str.strip()
        properties_df["city"] = properties_df["city"].astype(str).str.strip()
        properties_df["locality"] = properties_df["locality"].astype(str).str.strip()
        properties_df["bedrooms"] = pd.to_numeric(properties_df["bedrooms"], errors="coerce").fillna(0).astype(int)
        properties_df["area_sqft"] = pd.to_numeric(properties_df["area_sqft"], errors="coerce").fillna(0.0)
        properties_df["asking_price"] = pd.to_numeric(properties_df["asking_price"], errors="coerce").fillna(0.0)
        properties_df.loc[properties_df["asking_price"] < 0, "asking_price"] = 0.0
        properties_df.loc[properties_df["area_sqft"] < 0, "area_sqft"] = 0.0
        properties_df["listing_date"] = pd.to_datetime(properties_df["listing_date"]).dt.date
        properties_df["listing_status"] = properties_df["listing_status"].astype(str).str.strip()
        
        # Clean, validate, deduplicate and standardize Leads
        leads_df["lead_id"] = leads_df["lead_id"].astype(str).str.strip()
        leads_df = leads_df.drop_duplicates(subset=["lead_id"])
        leads_df["lead_name"] = leads_df["lead_name"].astype(str).str.strip()
        leads_df["property_type_interest"] = leads_df["property_type_interest"].astype(str).str.strip()
        leads_df["city"] = leads_df["city"].astype(str).str.strip()
        leads_df["lead_source"] = leads_df["lead_source"].astype(str).str.strip()
        leads_df["inquiry_date"] = pd.to_datetime(leads_df["inquiry_date"]).dt.date
        leads_df["budget_min"] = pd.to_numeric(leads_df["budget_min"], errors="coerce").fillna(0.0)
        leads_df["budget_max"] = pd.to_numeric(leads_df["budget_max"], errors="coerce").fillna(0.0)
        leads_df.loc[leads_df["budget_min"] < 0, "budget_min"] = 0.0
        leads_df.loc[leads_df["budget_max"] < 0, "budget_max"] = 0.0
        leads_df["lead_status"] = leads_df["lead_status"].astype(str).str.strip()
        leads_df["phone"] = leads_df["phone"].astype(str).str.strip()
        
        # Clean and standardize Site Visits
        visits_df["visit_id"] = visits_df["visit_id"].astype(str).str.strip()
        visits_df = visits_df.drop_duplicates(subset=["visit_id"])
        visits_df["lead_id"] = visits_df["lead_id"].astype(str).str.strip()
        visits_df["property_id"] = visits_df["property_id"].astype(str).str.strip()
        visits_df["visit_date"] = pd.to_datetime(visits_df["visit_date"]).dt.date
        visits_df["visit_feedback"] = visits_df["visit_feedback"].astype(str).str.strip()
        visits_df["visit_outcome"] = visits_df["visit_outcome"].astype(str).str.strip()
        visits_df["agent_id"] = visits_df["agent_id"].astype(str).str.strip()
        
        # Clean and standardize Deals
        deals_df["deal_id"] = deals_df["deal_id"].astype(str).str.strip()
        deals_df = deals_df.drop_duplicates(subset=["deal_id"])
        deals_df["lead_id"] = deals_df["lead_id"].astype(str).str.strip()
        deals_df["property_id"] = deals_df["property_id"].astype(str).str.strip()
        deals_df["deal_date"] = pd.to_datetime(deals_df["deal_date"]).dt.date
        deals_df["deal_status"] = deals_df["deal_status"].astype(str).str.strip()
        deals_df["sale_price"] = pd.to_numeric(deals_df["sale_price"], errors="coerce").fillna(0.0)
        deals_df.loc[deals_df["sale_price"] < 0, "sale_price"] = 0.0
        deals_df["commission_rate"] = pd.to_numeric(deals_df["commission_rate"], errors="coerce").fillna(0.02)
        deals_df["agent_id"] = deals_df["agent_id"].astype(str).str.strip()
        
        # Clean and standardize Agent Performance
        perf_df["performance_id"] = perf_df["performance_id"].astype(str).str.strip()
        perf_df = perf_df.drop_duplicates(subset=["performance_id"])
        perf_df["agent_id"] = perf_df["agent_id"].astype(str).str.strip()
        perf_df["period_month"] = perf_df["period_month"].astype(str).str.strip()
        perf_df["calls_made"] = pd.to_numeric(perf_df["calls_made"], errors="coerce").fillna(0).astype(int)
        perf_df["visits_conducted"] = pd.to_numeric(perf_df["visits_conducted"], errors="coerce").fillna(0).astype(int)
        perf_df["deals_closed"] = pd.to_numeric(perf_df["deals_closed"], errors="coerce").fillna(0).astype(int)
        perf_df["customer_rating"] = pd.to_numeric(perf_df["customer_rating"], errors="coerce").fillna(4.0)
        perf_df["marketing_spend"] = pd.to_numeric(perf_df["marketing_spend"], errors="coerce").fillna(0.0)
        
        # Clean and standardize Expenses
        expenses_df["expense_id"] = expenses_df["expense_id"].astype(str).str.strip()
        expenses_df["expense_date"] = pd.to_datetime(expenses_df["expense_date"]).dt.date
        expenses_df["project_id"] = expenses_df["project_id"].astype(str).str.strip()
        expenses_df["category"] = expenses_df["category"].astype(str).str.strip()
        expenses_df["amount"] = pd.to_numeric(expenses_df["amount"], errors="coerce").fillna(0.0)
        expenses_df["vendor"] = expenses_df["vendor"].astype(str).str.strip()
        
        return {
            "properties": properties_df,
            "leads": leads_df,
            "visits": visits_df,
            "deals": deals_df,
            "performance": perf_df,
            "expenses": expenses_df
        }

    @classmethod
    def seed_database_from_excel(cls, db: Session, file_path: str):
        """Seeds the database from clean Excel data if not already populated."""
        if db.query(Property).count() > 0:
            print("Database already contains property records. Skipping seeding.")
            return
            
        print(f"Reading and seeding real estate dataset from: {file_path}")
        dfs = cls.load_and_clean_excel(file_path)
        
        # Seed Properties
        properties = [
            Property(
                property_id=row["property_id"],
                property_type=row["property_type"],
                city=row["city"],
                locality=row["locality"],
                bedrooms=row["bedrooms"],
                area_sqft=row["area_sqft"],
                asking_price=row["asking_price"],
                listing_date=row["listing_date"],
                listing_status=row["listing_status"]
            )
            for _, row in dfs["properties"].iterrows()
        ]
        db.bulk_save_objects(properties)
        db.commit()
        print(f"Seeded {len(properties)} Properties.")
        
        # Seed Leads
        leads = [
            Lead(
                lead_id=row["lead_id"],
                lead_name=row["lead_name"],
                property_type_interest=row["property_type_interest"],
                city=row["city"],
                lead_source=row["lead_source"],
                inquiry_date=row["inquiry_date"],
                budget_min=row["budget_min"],
                budget_max=row["budget_max"],
                lead_status=row["lead_status"],
                phone=row["phone"]
            )
            for _, row in dfs["leads"].iterrows()
        ]
        db.bulk_save_objects(leads)
        db.commit()
        print(f"Seeded {len(leads)} Leads.")
        
        # Seed Site Visits
        visits = [
            SiteVisit(
                visit_id=row["visit_id"],
                lead_id=row["lead_id"],
                property_id=row["property_id"],
                visit_date=row["visit_date"],
                visit_feedback=row["visit_feedback"],
                visit_outcome=row["visit_outcome"],
                agent_id=row["agent_id"]
            )
            for _, row in dfs["visits"].iterrows()
        ]
        db.bulk_save_objects(visits)
        db.commit()
        print(f"Seeded {len(visits)} Site Visits.")
        
        # Seed Deals
        deals = [
            Deal(
                deal_id=row["deal_id"],
                lead_id=row["lead_id"],
                property_id=row["property_id"],
                deal_date=row["deal_date"],
                deal_status=row["deal_status"],
                sale_price=row["sale_price"],
                commission_rate=row["commission_rate"],
                agent_id=row["agent_id"]
            )
            for _, row in dfs["deals"].iterrows()
        ]
        db.bulk_save_objects(deals)
        db.commit()
        print(f"Seeded {len(deals)} Deals.")
        
        # Seed Agent Performance
        perfs = [
            AgentPerformance(
                performance_id=row["performance_id"],
                agent_id=row["agent_id"],
                period_month=row["period_month"],
                calls_made=row["calls_made"],
                visits_conducted=row["visits_conducted"],
                deals_closed=row["deals_closed"],
                customer_rating=row["customer_rating"],
                marketing_spend=row["marketing_spend"]
            )
            for _, row in dfs["performance"].iterrows()
        ]
        db.bulk_save_objects(perfs)
        db.commit()
        print(f"Seeded {len(perfs)} Agent Performance records.")
        
        # Seed Expenses
        expenses = [
            Expense(
                expense_id=row["expense_id"],
                expense_date=row["expense_date"],
                project_id=row["project_id"],
                category=row["category"],
                amount=row["amount"],
                vendor=row["vendor"]
            )
            for _, row in dfs["expenses"].iterrows()
        ]
        db.bulk_save_objects(expenses)
        db.commit()
        print(f"Seeded {len(expenses)} Operational Expenses.")
        print("Database seeding completed successfully!")

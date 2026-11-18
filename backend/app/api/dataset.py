import os
import shutil
import uuid
import logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import Optional, List
import pandas as pd
from ..core.database import get_db
from ..core.security import require_role, get_current_user
from ..models.user import User
from ..models.real_estate import Property, Lead, SiteVisit, Deal, AgentPerformance, Expense
from ..schemas.dataset import PropertyOut, LeadOut, SiteVisitOut, DealOut, ExpenseOut, DatasetSummaryOut
from ..services.data_processor import DataProcessor

logger = logging.getLogger("uvicorn.error")
router = APIRouter(prefix="/dataset", tags=["Dataset Management"])

@router.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    current_user: User = Depends(require_role(["admin", "manager"])),
    db: Session = Depends(get_db)
):
    """Admin/Manager-only: Upload an Excel (.xlsx) or CSV dataset file, clean data, and ingest into database."""
    filename_lower = (file.filename or "").lower()
    if not (filename_lower.endswith(".xlsx") or filename_lower.endswith(".xls") or filename_lower.endswith(".csv")):
        raise HTTPException(status_code=400, detail="Only Excel (.xlsx, .xls) or CSV files are supported")
        
    os.makedirs("uploads", exist_ok=True)
    safe_ext = ".xlsx" if filename_lower.endswith((".xlsx", ".xls")) else ".csv"
    safe_filename = f"{uuid.uuid4().hex}_{current_user.id}{safe_ext}"
    file_path = os.path.join("uploads", safe_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        if safe_ext == ".xlsx":
            dfs = DataProcessor.load_and_clean_excel(file_path)
            # Clear old records and replace
            db.query(SiteVisit).delete()
            db.query(Deal).delete()
            db.query(Lead).delete()
            db.query(Property).delete()
            db.query(AgentPerformance).delete()
            db.query(Expense).delete()
            db.commit()
            
            # Re-seed
            DataProcessor.seed_database_from_excel(db, file_path)
            
            return {
                "message": "Excel dataset successfully uploaded, validated, cleaned, and imported into database.",
                "uploaded_by": f"{current_user.full_name} ({current_user.role})",
                "sheets_processed": list(dfs.keys()),
                "properties_count": len(dfs["properties"]),
                "leads_count": len(dfs["leads"]),
                "visits_count": len(dfs["visits"]),
                "deals_count": len(dfs["deals"])
            }
        else:
            # Process single CSV file and persist into database
            csv_df = pd.read_csv(file_path)
            csv_df.columns = [c.strip().lower().replace(" ", "_") for c in csv_df.columns]
            cols = list(csv_df.columns)
            table_name = "unknown"
            inserted_count = 0
            
            def safe_date(val):
                if pd.isna(val):
                    return datetime.utcnow().date()
                try:
                    return pd.to_datetime(val).date()
                except Exception:
                    return datetime.utcnow().date()

            if any("prop" in c for c in cols):
                table_name = "properties"
                for _, row in csv_df.iterrows():
                    pid = str(row.get("property_id") or f"PROP_{uuid.uuid4().hex[:6].upper()}")
                    existing = db.query(Property).filter(Property.property_id == pid).first()
                    if not existing:
                        p = Property(
                            property_id=pid,
                            property_type=str(row.get("property_type") or "Apartment"),
                            city=str(row.get("city") or "Mumbai"),
                            locality=str(row.get("locality") or "Central"),
                            bedrooms=int(row.get("bedrooms") or 2),
                            area_sqft=float(row.get("area_sqft") or 1000.0),
                            asking_price=float(row.get("asking_price") or 5000000.0),
                            listing_date=safe_date(row.get("listing_date")),
                            listing_status=str(row.get("listing_status") or "Available")
                        )
                        db.add(p)
                        inserted_count += 1
            elif any("lead" in c for c in cols):
                table_name = "leads"
                for _, row in csv_df.iterrows():
                    lid = str(row.get("lead_id") or f"LEAD_{uuid.uuid4().hex[:6].upper()}")
                    existing = db.query(Lead).filter(Lead.lead_id == lid).first()
                    if not existing:
                        lead = Lead(
                            lead_id=lid,
                            lead_name=str(row.get("lead_name") or "Inquiry Lead"),
                            property_type_interest=str(row.get("property_type_interest") or "Apartment"),
                            city=str(row.get("city") or "Mumbai"),
                            lead_source=str(row.get("lead_source") or "Campaign"),
                            inquiry_date=safe_date(row.get("inquiry_date")),
                            budget_min=float(row.get("budget_min") or 3000000.0),
                            budget_max=float(row.get("budget_max") or 8000000.0),
                            lead_status=str(row.get("lead_status") or "New"),
                            phone=str(row.get("phone") or "")
                        )
                        db.add(lead)
                        inserted_count += 1
            elif any("deal" in c for c in cols):
                table_name = "deals"
                for _, row in csv_df.iterrows():
                    did = str(row.get("deal_id") or f"DEAL_{uuid.uuid4().hex[:6].upper()}")
                    existing = db.query(Deal).filter(Deal.deal_id == did).first()
                    if not existing:
                        deal = Deal(
                            deal_id=did,
                            lead_id=str(row.get("lead_id") or "LEAD001"),
                            property_id=str(row.get("property_id") or "PROP001"),
                            deal_date=safe_date(row.get("deal_date")),
                            deal_status=str(row.get("deal_status") or "Closed Won"),
                            sale_price=float(row.get("sale_price") or 7500000.0),
                            commission_rate=float(row.get("commission_rate") or 0.02),
                            agent_id=str(row.get("agent_id") or "AGT001")
                        )
                        db.add(deal)
                        inserted_count += 1
            elif any("exp" in c for c in cols):
                table_name = "expenses"
                for _, row in csv_df.iterrows():
                    eid = str(row.get("expense_id") or f"EXP_{uuid.uuid4().hex[:6].upper()}")
                    existing = db.query(Expense).filter(Expense.expense_id == eid).first()
                    if not existing:
                        exp = Expense(
                            expense_id=eid,
                            expense_date=safe_date(row.get("expense_date")),
                            project_id=str(row.get("project_id") or "PRJ001"),
                            category=str(row.get("category") or "Advertising"),
                            amount=float(row.get("amount") or 50000.0),
                            vendor=str(row.get("vendor") or "Marketing Partner")
                        )
                        db.add(exp)
                        inserted_count += 1
            
            db.commit()
            return {
                "message": f"CSV dataset successfully processed, validated, and persisted for table: {table_name}.",
                "uploaded_by": f"{current_user.full_name} ({current_user.role})",
                "rows_detected": len(csv_df),
                "rows_inserted": inserted_count,
                "table_detected": table_name
            }
    except Exception as e:
        db.rollback()
        logger.error(f"Dataset upload processing error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to parse dataset file. Please verify schema structure.")

@router.get("/summary", response_model=DatasetSummaryOut)
def get_dataset_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tot_props = db.query(Property).count()
    tot_leads = db.query(Lead).count()
    tot_visits = db.query(SiteVisit).count()
    tot_deals = db.query(Deal).count()
    tot_perf = db.query(AgentPerformance).count()
    tot_expenses = db.query(Expense).count()
    
    cities = [c[0] for c in db.query(Property.city).distinct().all()]
    ptypes = [p[0] for p in db.query(Property.property_type).distinct().all()]
    
    props = db.query(Property).all()
    inv_val = sum([p.asking_price for p in props]) if props else 0.0
    
    closed_deals = db.query(Deal).filter(Deal.deal_status == "Closed Won").all()
    sales_vol = sum([d.sale_price for d in closed_deals]) if closed_deals else 0.0
    
    expenses = db.query(Expense).all()
    exp_amt = sum([e.amount for e in expenses]) if expenses else 0.0
    
    return {
        "total_properties": tot_props,
        "total_leads": tot_leads,
        "total_visits": tot_visits,
        "total_deals": tot_deals,
        "total_agent_records": tot_perf,
        "total_expenses": tot_expenses,
        "date_coverage": "May 1, 2026 – October 31, 2026",
        "cities": cities,
        "property_types": ptypes,
        "total_inventory_value": round(inv_val, 2),
        "total_closed_sales_volume": round(sales_vol, 2),
        "total_expenses_amount": round(exp_amt, 2)
    }

@router.get("/properties", response_model=List[PropertyOut])
def get_properties(
    city: Optional[str] = None,
    property_type: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Property)
    if city:
        query = query.filter(Property.city.ilike(f"%{city}%"))
    if property_type:
        query = query.filter(Property.property_type == property_type)
    if status:
        query = query.filter(Property.listing_status == status)
    return query.offset(skip).limit(limit).all()

@router.get("/leads", response_model=List[LeadOut])
def get_leads(
    city: Optional[str] = None,
    status: Optional[str] = None,
    source: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Lead)
    if city:
        query = query.filter(Lead.city.ilike(f"%{city}%"))
    if status:
        query = query.filter(Lead.lead_status == status)
    if source:
        query = query.filter(Lead.lead_source == source)
    return query.offset(skip).limit(limit).all()

@router.get("/deals", response_model=List[DealOut])
def get_deals(
    status: Optional[str] = None,
    agent_id: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Deal)
    if status:
        query = query.filter(Deal.deal_status == status)
    if agent_id:
        query = query.filter(Deal.agent_id == agent_id)
    return query.offset(skip).limit(limit).all()

@router.get("/visits", response_model=List[SiteVisitOut])
def get_visits(
    outcome: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(SiteVisit)
    if outcome:
        query = query.filter(SiteVisit.visit_outcome == outcome)
    return query.offset(skip).limit(limit).all()

@router.get("/expenses", response_model=List[ExpenseOut])
def get_expenses(
    category: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Expense)
    if category:
        query = query.filter(Expense.category == category)
    return query.offset(skip).limit(limit).all()

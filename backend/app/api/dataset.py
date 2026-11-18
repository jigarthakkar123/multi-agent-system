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
            # Process single CSV file with strict schema validation (Zero-Hallucination Ingestion)
            csv_df = pd.read_csv(file_path)
            csv_df.columns = [c.strip().lower().replace(" ", "_") for c in csv_df.columns]
            cols = list(csv_df.columns)
            table_name = "unknown"
            inserted_count = 0
            rejection_reasons = []
            
            def parse_date(val):
                if pd.isna(val) or val is None or str(val).strip() == "":
                    return None
                try:
                    return pd.to_datetime(val).date()
                except Exception:
                    return None

            def is_empty(val):
                return pd.isna(val) or val is None or str(val).strip() == ""

            # Prioritize specific table column signatures
            if any("deal" in c for c in cols) or "sale_price" in cols:
                table_name = "deals"
            elif any("prop" in c for c in cols) and ("asking_price" in cols or "area_sqft" in cols or "property_type" in cols):
                table_name = "properties"
            elif any("lead" in c for c in cols) and ("budget_min" in cols or "inquiry_date" in cols or "lead_name" in cols):
                table_name = "leads"
            elif any("exp" in c for c in cols) or ("amount" in cols and "vendor" in cols):
                table_name = "expenses"
            elif any("prop" in c for c in cols):
                table_name = "properties"
            elif any("lead" in c for c in cols):
                table_name = "leads"

            if table_name == "properties":
                for idx, row in csv_df.iterrows():
                    missing = []
                    pid = row.get("property_id")
                    if is_empty(pid): missing.append("property_id")
                    ptype = row.get("property_type")
                    if is_empty(ptype): missing.append("property_type")
                    city = row.get("city")
                    if is_empty(city): missing.append("city")
                    area = row.get("area_sqft")
                    if is_empty(area): missing.append("area_sqft")
                    price = row.get("asking_price")
                    if is_empty(price): missing.append("asking_price")
                    ldate = parse_date(row.get("listing_date"))
                    if not ldate: missing.append("listing_date")

                    if missing:
                        rejection_reasons.append(f"Row {idx+1}: Rejected due to missing required field(s): {', '.join(missing)}")
                        continue

                    try:
                        area_f = float(area)
                        price_f = float(price)
                    except ValueError:
                        rejection_reasons.append(f"Row {idx+1}: Rejected due to non-numeric area_sqft or asking_price")
                        continue

                    existing = db.query(Property).filter(Property.property_id == str(pid).strip()).first()
                    if not existing:
                        p = Property(
                            property_id=str(pid).strip(),
                            property_type=str(ptype).strip(),
                            city=str(city).strip(),
                            locality=str(row.get("locality") or "Central").strip(),
                            bedrooms=int(row.get("bedrooms")) if not is_empty(row.get("bedrooms")) else 0,
                            area_sqft=area_f,
                            asking_price=price_f,
                            listing_date=ldate,
                            listing_status=str(row.get("listing_status") or "Available").strip()
                        )
                        db.add(p)
                        inserted_count += 1

            elif table_name == "leads":
                for idx, row in csv_df.iterrows():
                    missing = []
                    lid = row.get("lead_id")
                    if is_empty(lid): missing.append("lead_id")
                    lname = row.get("lead_name")
                    if is_empty(lname): missing.append("lead_name")
                    city = row.get("city")
                    if is_empty(city): missing.append("city")
                    idate = parse_date(row.get("inquiry_date"))
                    if not idate: missing.append("inquiry_date")
                    bmin = row.get("budget_min")
                    if is_empty(bmin): missing.append("budget_min")
                    bmax = row.get("budget_max")
                    if is_empty(bmax): missing.append("budget_max")

                    if missing:
                        rejection_reasons.append(f"Row {idx+1}: Rejected due to missing required field(s): {', '.join(missing)}")
                        continue

                    try:
                        bmin_f = float(bmin)
                        bmax_f = float(bmax)
                    except ValueError:
                        rejection_reasons.append(f"Row {idx+1}: Rejected due to non-numeric budget values")
                        continue

                    existing = db.query(Lead).filter(Lead.lead_id == str(lid).strip()).first()
                    if not existing:
                        lead = Lead(
                            lead_id=str(lid).strip(),
                            lead_name=str(lname).strip(),
                            property_type_interest=str(row.get("property_type_interest") or "Apartment").strip(),
                            city=str(city).strip(),
                            lead_source=str(row.get("lead_source") or "Campaign").strip(),
                            inquiry_date=idate,
                            budget_min=bmin_f,
                            budget_max=bmax_f,
                            lead_status=str(row.get("lead_status") or "New").strip(),
                            phone=str(row.get("phone") or "").strip()
                        )
                        db.add(lead)
                        inserted_count += 1

            elif table_name == "deals":
                for idx, row in csv_df.iterrows():
                    missing = []
                    did = row.get("deal_id")
                    if is_empty(did): missing.append("deal_id")
                    lid = row.get("lead_id")
                    if is_empty(lid): missing.append("lead_id")
                    pid = row.get("property_id")
                    if is_empty(pid): missing.append("property_id")
                    ddate = parse_date(row.get("deal_date"))
                    if not ddate: missing.append("deal_date")
                    sprice = row.get("sale_price")
                    if is_empty(sprice): missing.append("sale_price")
                    crate = row.get("commission_rate")
                    if is_empty(crate): missing.append("commission_rate")
                    aid = row.get("agent_id")
                    if is_empty(aid): missing.append("agent_id")

                    if missing:
                        rejection_reasons.append(f"Row {idx+1}: Rejected due to missing required field(s): {', '.join(missing)}")
                        continue

                    try:
                        sprice_f = float(sprice)
                        crate_f = float(crate)
                    except ValueError:
                        rejection_reasons.append(f"Row {idx+1}: Rejected due to non-numeric sale_price or commission_rate")
                        continue

                    existing = db.query(Deal).filter(Deal.deal_id == str(did).strip()).first()
                    if not existing:
                        deal = Deal(
                            deal_id=str(did).strip(),
                            lead_id=str(lid).strip(),
                            property_id=str(pid).strip(),
                            deal_date=ddate,
                            deal_status=str(row.get("deal_status") or "Closed Won").strip(),
                            sale_price=sprice_f,
                            commission_rate=crate_f,
                            agent_id=str(aid).strip()
                        )
                        db.add(deal)
                        inserted_count += 1

            elif table_name == "expenses":
                for idx, row in csv_df.iterrows():
                    missing = []
                    eid = row.get("expense_id")
                    if is_empty(eid): missing.append("expense_id")
                    edate = parse_date(row.get("expense_date"))
                    if not edate: missing.append("expense_date")
                    prjid = row.get("project_id")
                    if is_empty(prjid): missing.append("project_id")
                    cat = row.get("category")
                    if is_empty(cat): missing.append("category")
                    amt = row.get("amount")
                    if is_empty(amt): missing.append("amount")

                    if missing:
                        rejection_reasons.append(f"Row {idx+1}: Rejected due to missing required field(s): {', '.join(missing)}")
                        continue

                    try:
                        amt_f = float(amt)
                    except ValueError:
                        rejection_reasons.append(f"Row {idx+1}: Rejected due to non-numeric expense amount")
                        continue

                    existing = db.query(Expense).filter(Expense.expense_id == str(eid).strip()).first()
                    if not existing:
                        exp = Expense(
                            expense_id=str(eid).strip(),
                            expense_date=edate,
                            project_id=str(prjid).strip(),
                            category=str(cat).strip(),
                            amount=amt_f,
                            vendor=str(row.get("vendor") or "").strip()
                        )
                        db.add(exp)
                        inserted_count += 1
                    missing = []
                    eid = row.get("expense_id")
                    if is_empty(eid): missing.append("expense_id")
                    edate = parse_date(row.get("expense_date"))
                    if not edate: missing.append("expense_date")
                    prjid = row.get("project_id")
                    if is_empty(prjid): missing.append("project_id")
                    cat = row.get("category")
                    if is_empty(cat): missing.append("category")
                    amt = row.get("amount")
                    if is_empty(amt): missing.append("amount")

                    if missing:
                        rejection_reasons.append(f"Row {idx+1}: Rejected due to missing required field(s): {', '.join(missing)}")
                        continue

                    try:
                        amt_f = float(amt)
                    except ValueError:
                        rejection_reasons.append(f"Row {idx+1}: Rejected due to non-numeric expense amount")
                        continue

                    existing = db.query(Expense).filter(Expense.expense_id == str(eid).strip()).first()
                    if not existing:
                        exp = Expense(
                            expense_id=str(eid).strip(),
                            expense_date=edate,
                            project_id=str(prjid).strip(),
                            category=str(cat).strip(),
                            amount=amt_f,
                            vendor=str(row.get("vendor") or "").strip()
                        )
                        db.add(exp)
                        inserted_count += 1

            db.commit()
            return {
                "message": f"CSV dataset successfully processed with strict zero-hallucination validation for table: {table_name}.",
                "uploaded_by": f"{current_user.full_name} ({current_user.role})",
                "rows_detected": len(csv_df),
                "rows_inserted": inserted_count,
                "rows_skipped": len(rejection_reasons),
                "rejection_reasons": rejection_reasons[:10],
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

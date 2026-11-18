import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from ..core.database import get_db
from ..models.real_estate import Property, Lead, SiteVisit, Deal, AgentPerformance, Expense
from ..schemas.dataset import PropertyOut, LeadOut, SiteVisitOut, DealOut, ExpenseOut, DatasetSummaryOut
from ..services.data_processor import DataProcessor

router = APIRouter(prefix="/dataset", tags=["Dataset Management"])

@router.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Uploads an Excel (.xlsx) or CSV dataset file, cleans data, and updates the database."""
    if not file.filename.endswith((".xlsx", ".xls", ".csv")):
        raise HTTPException(status_code=400, detail="Only Excel (.xlsx, .xls) or CSV files are supported")
        
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # If it's an Excel workbook with sheets
        if file.filename.endswith((".xlsx", ".xls")):
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
                "message": "Dataset successfully uploaded, cleaned, and imported into database.",
                "sheets_processed": list(dfs.keys()),
                "properties_count": len(dfs["properties"]),
                "leads_count": len(dfs["leads"]),
                "visits_count": len(dfs["visits"]),
                "deals_count": len(dfs["deals"])
            }
        else:
            return {"message": "CSV uploaded. Please ensure multi-sheet Excel is uploaded for full 6-agent analysis."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error parsing dataset: {str(e)}")

@router.get("/summary", response_model=DatasetSummaryOut)
def get_dataset_summary(db: Session = Depends(get_db)):
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
    db: Session = Depends(get_db)
):
    query = db.query(Expense)
    if category:
        query = query.filter(Expense.category == category)
    return query.offset(skip).limit(limit).all()

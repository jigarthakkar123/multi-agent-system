import os
import re
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .core.config import settings
from .core.database import engine, Base, SessionLocal
from .core.security import get_password_hash
from .models.user import User
from .models.business_profile import BusinessProfile
from .services.data_processor import DataProcessor
from .agents.crew_orchestrator import CrewOrchestrator
from .api.api_router import api_router

# Initialize FastAPI App with complete OpenAPI Documentation
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        "Full-Stack Multi-Agent AI Business Operations & Decision Intelligence Platform for Real Estate. "
        "Orchestrates 6 specialized CrewAI autonomous agents (Data Analyst, Marketing, Finance, Operations, Strategy, Verification) "
        "to analyze listings, customer leads, site visits, deals, and expenses for executive decision intelligence."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Normalize duplicate slashes in incoming request paths
@app.middleware("http")
async def normalize_slashes_middleware(request: Request, call_next):
    if "//" in request.scope["path"]:
        request.scope["path"] = re.sub(r"/+", "/", request.scope["path"])
    return await call_next(request)

# Enable CORS for Netlify frontend, Render domains and local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router under both /api and root fallback
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(api_router, prefix="", include_in_schema=False)

@app.on_event("startup")
def on_startup():
    """Initializes tables, seeds demo users, imports Excel dataset, and builds baseline BI intelligence."""
    print("Initializing Database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Automatic backward-compatible database schema migration check
    try:
        from sqlalchemy import text, inspect
        inspector = inspect(engine)
        if "analysis_reports" in inspector.get_table_names():
            columns = [c["name"] for c in inspector.get_columns("analysis_reports")]
            if "verification_details_json" not in columns:
                print("Applying schema migration: Adding verification_details_json column to analysis_reports...")
                with engine.connect() as conn:
                    if "postgres" in str(engine.url).lower():
                        conn.execute(text("ALTER TABLE analysis_reports ADD COLUMN IF NOT EXISTS verification_details_json JSON;"))
                    else:
                        conn.execute(text("ALTER TABLE analysis_reports ADD COLUMN verification_details_json JSON;"))
                    conn.commit()
    except Exception as e:
        print(f"Schema migration notice: {e}")
    
    db = SessionLocal()
    try:
        # 1. Seed Default Admin & Manager Users
        admin_user = db.query(User).filter(User.email == "admin@realtyintelligence.ai").first()
        if not admin_user:
            admin_user = User(
                email="admin@realtyintelligence.ai",
                hashed_password=get_password_hash("Admin@2026!"),
                full_name="Chief Executive Officer",
                role="admin",
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            
            # Create Default Business Profile
            profile = BusinessProfile(
                user_id=admin_user.id,
                company_name="Apex Realty Intelligence Corp",
                industry="Real Estate - Property & Sales Intelligence",
                team_size=55,
                business_goals="Drive 25% annual revenue growth, reduce CAC by 18%, and optimize agent velocity across Western India hubs."
            )
            db.add(profile)
            db.commit()
            print("Seeded default administrator: admin@realtyintelligence.ai (password: Admin@2026!)")

        manager_user = db.query(User).filter(User.email == "manager@realtyintelligence.ai").first()
        if not manager_user:
            manager_user = User(
                email="manager@realtyintelligence.ai",
                hashed_password=get_password_hash("Manager@2026!"),
                full_name="Senior Real Estate Operations Manager",
                role="manager",
                is_active=True
            )
            db.add(manager_user)
            db.commit()
            print("Seeded default manager: manager@realtyintelligence.ai (password: Manager@2026!)")

        # 2. Seed Dataset from Excel
        excel_path = os.path.join("data", "real_estate_dataset.xlsx")
        if not os.path.exists(excel_path):
            excel_path = os.path.join(os.path.dirname(__file__), "..", "data", "real_estate_dataset.xlsx")
            
        if os.path.exists(excel_path):
            DataProcessor.seed_database_from_excel(db, excel_path)
        else:
            print(f"Notice: Excel dataset not found at {excel_path}. Please upload via /api/dataset/upload.")

        # 3. Pre-generate initial Multi-Agent Baseline Report if none exists
        from .models.report import AnalysisReport
        if db.query(AnalysisReport).count() == 0:
            print("Running initial Multi-Agent intelligence baseline...")
            orchestrator = CrewOrchestrator(db)
            orchestrator.run_multi_agent_pipeline(execution_mode="sequential")
            print("Baseline Multi-Agent Decision Intelligence Report generated!")
            
    except Exception as e:
        print(f"Startup initialization notice: {e}")
    finally:
        db.close()

import logging
logger = logging.getLogger("uvicorn.error")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Internal server error processing {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please contact the administrator.", "path": str(request.url.path)}
    )

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "industry": "Real Estate - Property & Sales Intelligence",
        "dataset_period": "May 1, 2026 – October 31, 2026"
    }

@app.get("/", tags=["Root"])
def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "documentation": "/docs",
        "health": "/health",
        "api_prefix": settings.API_V1_STR
    }

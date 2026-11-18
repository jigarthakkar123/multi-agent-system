from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.security import get_current_user
from ..models.user import User
from ..models.business_profile import BusinessProfile
from ..schemas.business_profile import BusinessProfileOut, BusinessProfileUpdate

router = APIRouter(prefix="/profile", tags=["Business Profile"])

@router.get("", response_model=BusinessProfileOut)
def get_business_profile(db: Session = Depends(get_db)):
    profile = db.query(BusinessProfile).first()
    if not profile:
        profile = BusinessProfile()
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

@router.put("", response_model=BusinessProfileOut)
def update_business_profile(
    profile_in: BusinessProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(BusinessProfile).first()
    if not profile:
        profile = BusinessProfile(user_id=current_user.id)
        db.add(profile)
        
    profile.company_name = profile_in.company_name
    profile.industry = profile_in.industry
    profile.team_size = profile_in.team_size
    profile.business_goals = profile_in.business_goals
    
    db.commit()
    db.refresh(profile)
    return profile

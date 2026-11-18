from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, EmailStr
from ..core.database import get_db
from ..core.security import require_role
from ..models.user import User
from ..schemas.auth import UserOut

router = APIRouter(prefix="/users", tags=["User Management (Admin)"])

class UserRoleUpdate(BaseModel):
    role: str

class UserStatusUpdate(BaseModel):
    is_active: bool

@router.get("", response_model=List[UserOut])
def list_users(
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Admin-only: List all registered platform users and their roles."""
    return db.query(User).order_by(User.created_at.desc()).all()

@router.patch("/{user_id}/role", response_model=UserOut)
def update_user_role(
    user_id: int,
    role_in: UserRoleUpdate,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Admin-only: Update a user's role (admin, manager, analyst, agent)."""
    valid_roles = ["admin", "manager", "analyst", "agent"]
    if role_in.role not in valid_roles:
        raise HTTPException(status_code=400, detail=f"Invalid role. Must be one of {valid_roles}")
        
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.role = role_in.role
    db.commit()
    db.refresh(user)
    return user

@router.patch("/{user_id}/status", response_model=UserOut)
def update_user_status(
    user_id: int,
    status_in: UserStatusUpdate,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Admin-only: Activate or deactivate a user account."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot deactivate your own administrator account")
        
    user.is_active = status_in.is_active
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Admin-only: Remove a user from the platform."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own administrator account")
        
    db.delete(user)
    db.commit()
    return {"message": f"User #{user_id} deleted successfully"}

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta
from .. import models, schemas_admin
from ..database import get_db
from ..auth import get_current_admin_user

router = APIRouter(prefix="/admin", tags=["admin"])


# ---------------------------
# Get all users
# ---------------------------
@router.get("/users", response_model=List[schemas_admin.UserAdmin])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_admin: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all users (admin only)"""
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


# ---------------------------
# Get user statistics
# ---------------------------
@router.get("/users/stats", response_model=schemas_admin.UserStats)
def get_user_stats(
    current_admin: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get user statistics (admin only)"""
    total = db.query(models.User).count()
    active = db.query(models.User).filter(models.User.is_active == True).count()
    admins = db.query(models.User).filter(models.User.is_admin == True).count()

    # Users created in last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    new_users = db.query(models.User).filter(
        models.User.created_at >= thirty_days_ago
    ).count()

    return {
        "total_users": total,
        "active_users": active,
        "admin_users": admins,
        "new_users_this_month": new_users
    }


# ---------------------------
# Get specific user
# ---------------------------
@router.get("/users/{user_id}", response_model=schemas_admin.UserAdmin)
def get_user(
    user_id: int,
    current_admin: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get specific user (admin only)"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ---------------------------
# Update user
# ---------------------------
@router.patch("/users/{user_id}", response_model=schemas_admin.UserAdmin)
def update_user(
    user_id: int,
    user_update: schemas_admin.UserUpdate,
    current_admin: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update user (admin only)"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Prevent admin from deactivating themselves
    if user.id == current_admin.id and user_update.is_active == False:
        raise HTTPException(
            status_code=400,
            detail="Cannot deactivate your own account"
        )

    # Update fields
    if user_update.is_active is not None:
        user.is_active = user_update.is_active
    if user_update.is_admin is not None:
        user.is_admin = user_update.is_admin

    db.commit()
    db.refresh(user)
    return user


# ---------------------------
# Delete user
# ---------------------------
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_admin: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete user (admin only)"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Prevent admin from deleting themselves
    if user.id == current_admin.id:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete your own account"
        )

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

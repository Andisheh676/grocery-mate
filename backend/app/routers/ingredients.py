from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from .. import models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@router.get("/", response_model=List[schemas.Ingredient])
def get_ingredients(
    location: str = None,
    current_user: models.User = Depends(get_current_user),  # user-specific
    db: Session = Depends(get_db)
):
    """Get all ingredients for current user, optionally filtered by location (Fridge/Pantry)"""
    query = db.query(models.Ingredient).filter(models.Ingredient.user_id == current_user.id)
    if location:
        query = query.filter(models.Ingredient.location == location)
    return query.all()


@router.get("/{ingredient_id}", response_model=schemas.Ingredient)
def get_ingredient(
    ingredient_id: int,
    current_user: models.User = Depends(get_current_user),  # user-specific
    db: Session = Depends(get_db)
):
    """Get a specific ingredient by ID for current user"""
    ingredient = db.query(models.Ingredient).filter(
        models.Ingredient.id == ingredient_id,
        models.Ingredient.user_id == current_user.id
    ).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient


@router.post("/", response_model=schemas.Ingredient)
def create_ingredient(
    ingredient: schemas.IngredientCreate,
    current_user: models.User = Depends(get_current_user),  # user-specific
    db: Session = Depends(get_db)
):
    """Create a new ingredient for current user"""
    existing = db.query(models.Ingredient).filter(
        models.Ingredient.name == ingredient.name,
        models.Ingredient.user_id == current_user.id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ingredient already exists")

    db_ingredient = models.Ingredient(
        **ingredient.model_dump(),
        user_id=current_user.id
    )
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient


@router.put("/{ingredient_id}", response_model=schemas.Ingredient)
def update_ingredient(
    ingredient_id: int,
    ingredient: schemas.IngredientUpdate,
    current_user: models.User = Depends(get_current_user),  # user-specific
    db: Session = Depends(get_db)
):
    """Update an ingredient for current user"""
    db_ingredient = db.query(models.Ingredient).filter(
        models.Ingredient.id == ingredient_id,
        models.Ingredient.user_id == current_user.id
    ).first()
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    update_data = ingredient.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_ingredient, key, value)

    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient


@router.delete("/{ingredient_id}")
def delete_ingredient(
    ingredient_id: int,
    current_user: models.User = Depends(get_current_user),  # user-specific
    db: Session = Depends(get_db)
):
    """Delete an ingredient for current user"""
    db_ingredient = db.query(models.Ingredient).filter(
        models.Ingredient.id == ingredient_id,
        models.Ingredient.user_id == current_user.id
    ).first()
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    db.delete(db_ingredient)
    db.commit()
    return {"message": "Ingredient deleted successfully"}


@router.get("/expiring/soon", response_model=List[schemas.Ingredient])
def get_expiring_soon(
    days: int = 7,
    current_user: models.User = Depends(get_current_user),  # user-specific
    db: Session = Depends(get_db)
):
    """Get ingredients for current user expiring within specified days"""
    expiry_threshold = datetime.now().date() + timedelta(days=days)

    ingredients = db.query(models.Ingredient).filter(
        models.Ingredient.user_id == current_user.id,
        models.Ingredient.expiry_date.isnot(None),
        models.Ingredient.expiry_date <= expiry_threshold
    ).all()
    return ingredients

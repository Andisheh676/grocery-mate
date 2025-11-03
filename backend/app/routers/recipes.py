from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.auth import get_current_user
from app.services.gemini_service import generate_recipe
import json

router = APIRouter(prefix="/recipes", tags=["recipes"])

# ---------------------------
# Get all recipes for current user
# ---------------------------
@router.get("/", response_model=List[schemas.Recipe])
def get_recipes(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(models.Recipe).filter(models.Recipe.user_id == current_user.id).all()


# ---------------------------
# Get a specific recipe by ID
# ---------------------------
@router.get("/{recipe_id}", response_model=schemas.Recipe)
def get_recipe(
    recipe_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    recipe = db.query(models.Recipe).filter(
        models.Recipe.id == recipe_id,
        models.Recipe.user_id == current_user.id
    ).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


# ---------------------------
# Generate a recipe using Gemini
# ---------------------------
@router.post("/generate", response_model=schemas.Recipe)
async def create_recipe(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ingredients = [
        {"name": "tomato", "quantity": "2", "unit": "pcs"},
        {"name": "onion", "quantity": "1", "unit": "pcs"}
    ]
    
    recipe_data = await generate_recipe(ingredients, preferences="vegan")
    
    if "error" in recipe_data:
        raise HTTPException(status_code=500, detail=f"Gemini error: {recipe_data['error']}")
    
    if not recipe_data.get("ingredients") or not recipe_data.get("instructions"):
        raise HTTPException(status_code=500, detail="Gemini returned invalid recipe data")

    def parse_time(t: str) -> int:
        try:
            return int(t.split()[0])
        except:
            return 0

    new_recipe = models.Recipe(
        name=recipe_data.get("name", "Unknown Recipe"),
        description=recipe_data.get("description", ""),
        ingredients=json.dumps(recipe_data.get("ingredients", [])),
        instructions=json.dumps(recipe_data.get("instructions", [])),
        prep_time=parse_time(recipe_data.get("prep_time", "0")),
        cook_time=parse_time(recipe_data.get("cook_time", "0")),
        servings=recipe_data.get("servings", 1),
        calories=recipe_data.get("calories", 0),
        difficulty=recipe_data.get("difficulty", "Unknown"),
        tags=json.dumps(recipe_data.get("tags", [])),
        user_id=current_user.id
    )
    
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    
    return new_recipe


# ---------------------------
# Seed sample recipes (for testing)
# ---------------------------
@router.post("/seed-sample")
def seed_sample_recipes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    sample_recipes = [
        {
            "name": "Tomato Pasta",
            "description": "Delicious tomato pasta",
            "ingredients": json.dumps([{"name": "tomato", "quantity": 2, "unit": "pcs"}]),
            "instructions": json.dumps(["Boil pasta", "Add tomato sauce"]),
            "prep_time": 10,
            "cook_time": 15,
            "servings": 2,
            "calories": 300,
            "difficulty": "Easy",
            "tags": json.dumps(["pasta", "vegan"]),
            "user_id": current_user.id
        }
    ]
    for r in sample_recipes:
        db_recipe = models.Recipe(**r)
        db.add(db_recipe)
    db.commit()
    return {"message": "Sample recipes added"}


# ---------------------------
# Match recipes based on ingredients
# ---------------------------
@router.get("/match/ingredients", response_model=List[schemas.Recipe])
def match_recipes(
    ingredients: List[str] = Query(...),
    db: Session = Depends(get_db)
):
    recipes = db.query(models.Recipe).all()
    matched = []

    for r in recipes:
        try:
            recipe_ingredients_json = json.loads(r.ingredients)
            recipe_ingredients = [
                i['name'] if isinstance(i, dict) and 'name' in i else str(i)
                for i in recipe_ingredients_json
            ]
            if all(ing in recipe_ingredients for ing in ingredients):
                matched.append(r)
        except Exception:
            # JSON خراب یا نامعتبر را نادیده می‌گیریم
            continue

    return matched

# ---------------------------
# Create a new recipe manually (used when AI-generated recipe is saved from frontend)
# ---------------------------
@router.post("/", response_model=schemas.Recipe)
def create_recipe_manual(
    recipe: schemas.RecipeCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_recipe = models.Recipe(
        name=recipe.name,
        description=recipe.description,
        ingredients=json.dumps(recipe.ingredients),
        instructions=json.dumps(recipe.instructions),
        prep_time=recipe.prep_time,
        cook_time=recipe.cook_time,
        servings=recipe.servings,
        calories=recipe.calories,
        difficulty=recipe.difficulty,
        tags=json.dumps(recipe.tags),
        user_id=current_user.id
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe

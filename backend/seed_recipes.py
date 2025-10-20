# file: seed_recipes.py
from datetime import datetime
import json
from app.database import get_db, Base, engine
from app import models

# ساخت جدول‌ها (اگه قبلا حذف شده باشه)
Base.metadata.create_all(bind=engine)

# گرفتن session
db = next(get_db())

# پیدا کردن اولین user برای login
current_user = db.query(models.User).first()
if not current_user:
    raise Exception("User not found! لطفا اول user بسازید.")

# لیست چند Recipe نمونه
recipes_data = [
    {
        "name": "Tomato & Onion Salad",
        "description": "Fresh and simple salad with tomato and onion.",
        "ingredients": ["2 medium tomatoes", "1 medium onion"],
        "instructions": [
            "Wash and chop the tomatoes.",
            "Peel and thinly slice the onion.",
            "Mix everything in a bowl and serve."
        ],
        "prep_time": 10,
        "cook_time": 0,
        "servings": 2,
        "calories": 80,
        "difficulty": "Easy",
        "tags": ["vegan", "salad", "quick"]
    },
    {
        "name": "Simple Avocado Toast",
        "description": "Quick breakfast with avocado on bread.",
        "ingredients": ["1 avocado", "2 slices of bread"],
        "instructions": [
            "Toast the bread slices.",
            "Mash the avocado and spread on toast.",
            "Add salt and pepper to taste."
        ],
        "prep_time": 5,
        "cook_time": 0,
        "servings": 1,
        "calories": 200,
        "difficulty": "Easy",
        "tags": ["vegan", "breakfast", "quick"]
    }
]

# ذخیره در جدول
for r in recipes_data:
    recipe = models.Recipe(
        name=r["name"],
        description=r["description"],
        ingredients=json.dumps(r["ingredients"]),
        instructions=json.dumps(r["instructions"]),
        prep_time=r["prep_time"],
        cook_time=r["cook_time"],
        servings=r["servings"],
        calories=r["calories"],
        difficulty=r["difficulty"],
        tags=json.dumps(r["tags"]),
        user_id=current_user.id
    )
    db.add(recipe)

db.commit()
print("Sample recipes added!")

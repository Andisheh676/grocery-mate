import asyncio
import json
from app import models
from app.database import get_db
from app.services.gemini_service import generate_recipe

# اتصال به DB
db = next(get_db())

# نمونه کاربر برای ذخیره recipe
current_user = db.query(models.User).first()

# تابع کمکی برای تبدیل prep_time / cook_time
def parse_time(t: str) -> int:
    try:
        return int(t.split()[0])
    except:
        return 0

# مواد اولیه
ingredients = [
    {"name": "tomato", "quantity": "2", "unit": "pcs"},
    {"name": "onion", "quantity": "1", "unit": "pcs"}
]

# تولید recipe با Gemini
recipe_data = asyncio.run(generate_recipe(ingredients, preferences="vegan"))

if "error" in recipe_data:
    print("Error:", recipe_data["error"])
else:
    new_recipe = models.Recipe(
        name=recipe_data.get("name", "Unknown Recipe"),
        description=recipe_data.get("description", ""),
        ingredients=json.dumps(recipe_data.get("ingredients", [])),
        instructions=json.dumps(recipe_data.get("instructions", [])),
        prep_time=parse_time(recipe_data.get("prep_time", "0")),
        servings=recipe_data.get("servings", 1),
        calories=recipe_data.get("calories", 0),
        is_healthy=True,
        user_id=current_user.id
    )

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    print(f"Recipe saved! ID: {new_recipe.id}, Name: {new_recipe.name}")

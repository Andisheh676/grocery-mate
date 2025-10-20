import os
import json
import asyncio
from typing import List, Dict, Optional
from dotenv import load_dotenv
import google.generativeai as genai
import logging

# بارگذاری متغیرهای محیطی از .env
load_dotenv()

# تنظیم logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# گرفتن کلید API از محیط
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

# تنظیم کلید برای Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# انتخاب مدل مناسب
model = genai.GenerativeModel('gemini-2.5-pro')

async def generate_recipe(ingredients: List[Dict], preferences: Optional[str] = None) -> Dict:
    try:
        ing_list = "\n".join([f"- {i['name']}: {i['quantity']} {i['unit']}" for i in ingredients])
        prompt = f"""Create a recipe using ONLY these ingredients:
{ing_list}

{f'Preferences: {preferences}' if preferences else ''}

Respond with ONLY valid JSON with fields:
name, description, ingredients, instructions, prep_time, cook_time, servings, calories, difficulty, tags.
"""
        # اجرای sync تابع generate_content در async با to_thread
        response = await asyncio.to_thread(model.generate_content, prompt)
        text = response.text.strip()
        
        # اضافه کردن پرینت برای دیباگ
        print("Gemini output:", text)   # <--- اینجا داخل تابع باشه

        # حذف markdown اضافی
        if text.startswith("```"):
            text = text.split('\n', 1)[1] if '\n' in text else text[3:]
        if text.endswith("```"):
            text = text[:-3]

        recipe = json.loads(text)
        return recipe

    except Exception as e:
        logger.error("❌ Error generating recipe: %s", e)
        return {"error": str(e)}

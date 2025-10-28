# schemas.py
from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, EmailStr


# ---------------------------
# Ingredient Schemas
# ---------------------------
class IngredientBase(BaseModel):
    name: str
    location: str
    quantity: float
    unit: str
    expiry_date: Optional[date] = None

class IngredientCreate(IngredientBase):
    category: Optional[str] = "Unknown"

class IngredientUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    expiry_date: Optional[date] = None
    category: Optional[str] = None   # اگر ستون category داری




class Ingredient(IngredientBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ---------------------------
# Shopping List Schemas
# ---------------------------
class ShoppingItemBase(BaseModel):
    item_name: str
    quantity: float
    unit: str
    is_purchased: bool = False

class ShoppingItemCreate(ShoppingItemBase):
    pass

class ShoppingItem(ShoppingItemBase):
    id: int
    shopping_list_id: int

    class Config:
        orm_mode = True

class ShoppingListBase(BaseModel):
    name: str

class ShoppingListCreate(ShoppingListBase):
    pass

class ShoppingList(ShoppingListBase):
    id: int
    created_at: datetime
    items: List[ShoppingItem] = []

    class Config:
        orm_mode = True


# ---------------------------
# Recipe Schemas
# ---------------------------
class RecipeBase(BaseModel):
    name: str
    description: Optional[str] = None
    ingredients: str  # JSON string
    instructions: str
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    servings: int = 2
    calories: Optional[int] = None
    difficulty: Optional[str] = None
    tags: Optional[str] = None
    is_healthy: bool = True

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# ---------------------------
# User Schemas
# ---------------------------
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_admin: bool = False
    is_active: bool = True
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        orm_mode = True


# ---------------------------
# Authentication Schemas
# ---------------------------
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

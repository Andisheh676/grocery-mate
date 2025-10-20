from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True) # NEW
    is_admin = Column(Boolean, default=False) # NEW
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True) # NEW

    # Relationships
    ingredients = relationship("Ingredient", back_populates="owner")
    shopping_lists = relationship("ShoppingList", back_populates="owner")
    recipes = relationship("Recipe", back_populates="owner")


class Ingredient(Base):
    __tablename__ = "ingredients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, nullable=False)
    location = Column(String, nullable=False)
    quantity = Column(Float, default=0)
    unit = Column(String, nullable=False)
    expiry_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="ingredients")


class ShoppingList(Base):
    __tablename__ = "shopping_lists"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    items = relationship("ShoppingItem", back_populates="shopping_list", cascade="all, delete-orphan")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="shopping_lists")


class ShoppingItem(Base):
    __tablename__ = "shopping_items"
    
    id = Column(Integer, primary_key=True, index=True)
    shopping_list_id = Column(Integer, ForeignKey("shopping_lists.id"))
    item_name = Column(String, nullable=False)
    quantity = Column(Float, default=1)
    unit = Column(String, nullable=False)
    is_purchased = Column(Boolean, default=False)
    shopping_list = relationship("ShoppingList", back_populates="items")


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    ingredients = Column(Text, nullable=False)
    instructions = Column(Text, nullable=False)
    prep_time = Column(Integer, default=0)
    cook_time = Column(Integer, default=0)   # اگر لازم داری
    servings = Column(Integer, default=2)
    calories = Column(Integer, nullable=True)
    is_healthy = Column(Boolean, default=True)
    difficulty = Column(String, default="Unknown")  # اضافه شد
    tags = Column(Text, default="[]")              # اگر لازم داری
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="recipes")

class News(Base):
    __tablename__ = "news" 

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True) # URL-friendly title
    summary = Column(Text) # Short description
    content = Column(Text, nullable=False) # Full article
    image_url = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)   

    # Relationship
    author = relationship("User") 
    
    
class PageContent(Base):
    __tablename__ = "page_content"
    
    id = Column(Integer, primary_key=True, index=True)
    page_key = Column(String, unique=True, index=True) # e.g., 'privacy', 'terms'
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    updated_by_id = Column(Integer, ForeignKey("users.id"))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    updated_by = relationship("User")
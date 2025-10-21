from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import re

from .. import models, schemas_news
from ..database import get_db
from ..auth import get_current_admin_user, get_current_active_user

router = APIRouter(prefix="/news", tags=["news"])

# --------------------------
# Utility function
# --------------------------
def create_slug(title: str) -> str:
    """Create URL-friendly slug from title"""
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug

# --------------------------
# PUBLIC ENDPOINTS (no auth required)
# --------------------------
@router.get("/public", response_model=List[schemas_news.NewsPublic])
def get_published_news(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Get all published news (public)"""
    news = (
        db.query(models.News)
        .filter(models.News.is_published == True)
        .order_by(models.News.published_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return news

@router.get("/public/{slug}", response_model=schemas_news.NewsPublic)
def get_news_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get specific news article by slug (public)"""
    news = (
        db.query(models.News)
        .filter(models.News.slug == slug, models.News.is_published == True)
        .first()
    )
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news

# --------------------------
# ADMIN ENDPOINTS (auth required)
# --------------------------
@router.get("/", response_model=List[schemas_news.News])
def get_all_news(
    skip: int = 0,
    limit: int = 100,
    current_admin: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Get all news articles (admin only)"""
    news = (
        db.query(models.News)
        .order_by(models.News.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return news

@router.post("/", response_model=schemas_news.News)
def create_news(
    news: schemas_news.NewsCreate,
    current_admin: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Create news article (admin only)"""
    # Generate slug
    slug = create_slug(news.title)
    # Check if slug exists
    existing = db.query(models.News).filter(models.News.slug == slug).first()
    if existing:
        # Append number to make unique
        counter = 1
        while db.query(models.News).filter(models.News.slug == f"{slug}-{counter}").first():
            counter += 1
        slug = f"{slug}-{counter}"
    
    # اگر image_url خالی یا "string" بود، مقدار پیش‌فرض بگذار
    image_url = news.image_url
    if not image_url or image_url == "string":
        image_url = "https://picsum.photos/200/150"

    db_news = models.News(
        **news.model_dump(),
        image_url=image_url,
        slug=slug,
        author_id=current_admin.id,
        published_at=datetime.utcnow() if news.is_published else None
    )
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news


@router.put("/{news_id}", response_model=schemas_news.News)
def update_news(
    news_id: int,
    news_update: schemas_news.NewsUpdate,
    current_admin: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Update news article (admin only)"""
    db_news = db.query(models.News).filter(models.News.id == news_id).first()
    if not db_news:
        raise HTTPException(status_code=404, detail="News not found")

    update_data = news_update.model_dump(exclude_unset=True)
    
    # Update slug if title changed
    if 'title' in update_data:
        update_data['slug'] = create_slug(update_data['title'])
    
    # Set published_at if publishing
    if 'is_published' in update_data and update_data['is_published'] and not db_news.published_at:
        update_data['published_at'] = datetime.utcnow()

    for key, value in update_data.items():
        setattr(db_news, key, value)

    db.commit()
    db.refresh(db_news)
    return db_news

@router.delete("/{news_id}")
def delete_news(
    news_id: int,
    current_admin: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Delete news article (admin only)"""
    db_news = db.query(models.News).filter(models.News.id == news_id).first()
    if not db_news:
        raise HTTPException(status_code=404, detail="News not found")

    db.delete(db_news)
    db.commit()
    return {"message": "News deleted successfully"}

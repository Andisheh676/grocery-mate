from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base schema for news
class NewsBase(BaseModel):
    title: str
    summary: Optional[str] = None
    content: str
    image_url: Optional[str] = None
    is_published: bool = False

# Schema for creating news
class NewsCreate(NewsBase):
    pass

# Schema for updating news
class NewsUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    is_published: Optional[bool] = None

# Full news schema (with author info)
class News(NewsBase):
    id: int
    slug: str
    author_id: int
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Public view of news (no author info)
class NewsPublic(BaseModel):
    """Public news view (no author info)"""
    id: int
    title: str
    slug: str
    summary: Optional[str]
    content: str
    image_url: Optional[str]
    published_at: Optional[datetime]

    class Config:
        from_attributes = True

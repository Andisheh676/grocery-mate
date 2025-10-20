from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base model for page content
class PageContentBase(BaseModel):
    title: str
    content: str

# Model for creating new page content
class PageContentCreate(PageContentBase):
    page_key: str

# Model for updating existing page content
class PageContentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# Model for internal use (with ID and timestamp)
class PageContent(PageContentBase):
    id: int
    page_key: str
    updated_at: datetime

    class Config:
        from_attributes = True

# Model for public view of page content
class PageContentPublic(BaseModel):
    """Public page view"""
    title: str
    content: str
    updated_at: datetime

    class Config:
        from_attributes = True

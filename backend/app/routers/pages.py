from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas_pages
from ..database import get_db
from ..auth import get_current_admin_user

router = APIRouter(prefix="/pages", tags=["pages"])

# -----------------------------
# PUBLIC ENDPOINTS
# -----------------------------
@router.get("/public/{page_key}", response_model=schemas_pages.PageContentPublic)
def get_page_content(page_key: str, db: Session = Depends(get_db)):
    """Get page content by key (public)"""
    page = db.query(models.PageContent).filter(
        models.PageContent.page_key == page_key
    ).first()
    if not page:
        # Return default content if page doesn't exist
        return {
            "title": page_key.capitalize(),
            "content": f"Content for {page_key} page is not available yet.",
            "updated_at": None
        }
    return page

# -----------------------------
# ADMIN ENDPOINTS
# -----------------------------
@router.get("/", response_model=List[schemas_pages.PageContent])
def get_all_pages(
    current_admin: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all pages (admin only)"""
    pages = db.query(models.PageContent).all()
    return pages

@router.post("/", response_model=schemas_pages.PageContent)
def create_page(
    page: schemas_pages.PageContentCreate,
    current_admin: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create page content (admin only)"""
    # Check if page key exists
    existing = db.query(models.PageContent).filter(
        models.PageContent.page_key == page.page_key
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Page key already exists")
    
    db_page = models.PageContent(
        **page.model_dump(),
        updated_by_id=current_admin.id
    )
    db.add(db_page)
    db.commit()
    db.refresh(db_page)
    return db_page

@router.put("/{page_key}", response_model=schemas_pages.PageContent)
def update_page(
    page_key: str,
    page_update: schemas_pages.PageContentUpdate,
    current_admin: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update page content (admin only)"""
    db_page = db.query(models.PageContent).filter(
        models.PageContent.page_key == page_key
    ).first()
    if not db_page:
        raise HTTPException(status_code=404, detail="Page not found")
    
    update_data = page_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_page, key, value)
    
    db_page.updated_by_id = current_admin.id
    db.commit()
    db.refresh(db_page)
    return db_page

@router.delete("/{page_key}")
def delete_page(
    page_key: str,
    current_admin: models.User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete page content (admin only)"""
    db_page = db.query(models.PageContent).filter(
        models.PageContent.page_key == page_key
    ).first()
    if not db_page:
        raise HTTPException(status_code=404, detail="Page not found")
    
    db.delete(db_page)
    db.commit()
    return {"message": "Page deleted successfully"}

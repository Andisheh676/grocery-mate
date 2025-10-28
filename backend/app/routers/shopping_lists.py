from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/shopping-lists", tags=["shopping-lists"])

@router.get("/", response_model=List[schemas.ShoppingList])
def get_shopping_lists(current_user: models.User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    return db.query(models.ShoppingList).filter(models.ShoppingList.user_id == current_user.id).all()

@router.get("/{list_id}", response_model=schemas.ShoppingList)
def get_shopping_list(list_id:int, current_user: models.User = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    shopping_list = db.query(models.ShoppingList).filter(
        models.ShoppingList.id == list_id,
        models.ShoppingList.user_id == current_user.id
    ).first()
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    return shopping_list

@router.post("/", response_model=schemas.ShoppingList)
def create_shopping_list(shopping_list:schemas.ShoppingListCreate,
                         current_user: models.User = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    db_list = models.ShoppingList(**shopping_list.dict(), user_id=current_user.id)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

@router.delete("/{list_id}")
def delete_shopping_list(list_id:int, current_user: models.User = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    db_list = db.query(models.ShoppingList).filter(
        models.ShoppingList.id==list_id,
        models.ShoppingList.user_id==current_user.id
    ).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    db.delete(db_list)
    db.commit()
    return {"message":"Shopping list deleted successfully"}

@router.post("/{list_id}/items", response_model=schemas.ShoppingItem)
def add_item_to_list(list_id:int, item:schemas.ShoppingItemCreate,
                     current_user: models.User = Depends(get_current_user),
                     db: Session = Depends(get_db)):
    shopping_list = db.query(models.ShoppingList).filter(
        models.ShoppingList.id==list_id,
        models.ShoppingList.user_id==current_user.id
    ).first()
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    db_item = models.ShoppingItem(**item.model_dump(), shopping_list_id=list_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put("/items/{item_id}", response_model=schemas.ShoppingItem)
def update_shopping_item(item_id:int, is_purchased:bool,
                         current_user: models.User = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    db_item = db.query(models.ShoppingItem).join(models.ShoppingList).filter(
        models.ShoppingItem.id==item_id,
        models.ShoppingList.user_id==current_user.id
    ).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Shopping item not found")
    db_item.is_purchased = is_purchased
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/items/{item_id}")
def delete_shopping_item(item_id:int, current_user: models.User = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    db_item = db.query(models.ShoppingItem).join(models.ShoppingList).filter(
        models.ShoppingItem.id==item_id,
        models.ShoppingList.user_id==current_user.id
    ).first()
   

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import crud
from app.schemas import CategoryCreate, Category

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[Category])
def read_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)

@router.get("/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    cat = db.query(crud.models.Category).filter(crud.models.Category.id == category_id).first()
    if cat is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat

@router.post("/", response_model=Category, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, category.title)

@router.put("/{category_id}", response_model=Category)
def update_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    db_cat = db.query(crud.models.Category).filter(crud.models.Category.id == category_id).first()
    if db_cat is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db_cat.title = category.title
    db.commit()
    db.refresh(db_cat)
    return db_cat

@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_cat = db.query(crud.models.Category).filter(crud.models.Category.id == category_id).first()
    if db_cat is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_cat)
    db.commit()
    return
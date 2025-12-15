from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.db import SessionLocal  
from app.db import crud  
from app.db.schemas import BookCreate, Book
from app.db.schemas import CategoryCreate, Category

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[Book])
def read_books(category_id: Optional[int] = None, db: Session = Depends(get_db)):
    if category_id is not None:
        return db.query(crud.models.Book).filter(crud.models.Book.category_id == category_id).all()
    return crud.get_books(db)

@router.get("/{book_id}", response_model=Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(crud.models.Book).filter(crud.models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=Book, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    cat = db.query(crud.models.Category).filter(crud.models.Category.id == book.category_id).first()
    if not cat:
        raise HTTPException(status_code=400, detail="Category not found")
    return crud.create_book(db, book.title, book.description, book.price, book.category_id, book.url)

@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(crud.models.Book).filter(crud.models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    cat = db.query(crud.models.Category).filter(crud.models.Category.id == book.category_id).first()
    if not cat:
        raise HTTPException(status_code=400, detail="Category not found")
    db_book.title = book.title
    db_book.description = book.description
    db_book.price = book.price
    db_book.url = book.url
    db_book.category_id = book.category_id
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(crud.models.Book).filter(crud.models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return
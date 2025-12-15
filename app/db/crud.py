from sqlalchemy.orm import Session
from .models import Category, Book

def get_categories(db):
    return db.query(models.Category).all()

def create_category(db, title):
    db_category = models.Category(title=title)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_books(db):
    return db.query(models.Book).all()

def create_book(db, title, description, price, category_id, url=""):
    db_book = models.Book(
        title=title,
        description=description,
        price=price,
        url=url,
        category_id=category_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    title: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        from_attributes = True

class BookBase(BaseModel):
    title: str
    description: str
    price: float
    url: str = ""
    category_id: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    class Config:
        from_attributes = True
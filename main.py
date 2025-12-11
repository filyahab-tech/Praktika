from app.db import SessionLocal
from app.crud import get_categories, get_books

db = SessionLocal()

print("Категории:")
for category in get_categories(db):
    print(f"- {category.title}")

print("\nКниги:")
for book in get_books(db):
    print(f"- {book.title} | {book.category.title} | {book.price} руб.")

db.close()

from sqlalchemy import text
from app.db import engine, Base, SessionLocal
from app.crud import create_category, create_book

Base.metadata.create_all(bind=engine)

db = SessionLocal()

db.execute(text("TRUNCATE TABLE books, categories RESTART IDENTITY CASCADE"))

programming = create_category(db, "Программирование")
science = create_category(db, "Наука")

create_book(db, "Python для начинающих", "Основы программирования на Python", 500.0, programming.id)
create_book(db, "Алгоритмы и структуры данных", "Классические алгоритмы", 700.0, programming.id)
create_book(db, "Космос", "Исследование Вселенной", 900.0, science.id)
create_book(db, "Биология клетки", "Основы клеточной биологии", 550.0, science.id)

db.close()
print("База данных инициализирована")

from fastapi import FastAPI
from app.api import books, categories

app = FastAPI(title="Book Store API")

app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
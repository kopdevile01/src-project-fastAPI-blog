from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.routers import categories
from app.db import get_db

app = FastAPI(title="FastAPI Blog API")
app.include_router(categories.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI blog API"}


@app.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"db": "ok"}

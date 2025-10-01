from fastapi import FastAPI
from sqlalchemy import text

from app.db import engine

app = FastAPI(title="FastAPI Blog API")


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI blog API"}


@app.get("/health/db")
def health_db():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"db": "ok"}

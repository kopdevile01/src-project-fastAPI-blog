from fastapi import FastAPI
from sqlalchemy import text

from app.routers import categories, auth, posts, uploads
from app.db import engine
from app.middleware.auth import JWTMiddleware

app = FastAPI(title="FastAPI Blog API")
app.add_middleware(JWTMiddleware)
app.include_router(categories.router)
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(uploads.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI blog API"}


@app.get("/health/db")
def health_db():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"db": "ok"}

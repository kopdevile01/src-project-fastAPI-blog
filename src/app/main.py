from fastapi import FastAPI

from app.middleware.auth import JWTMiddleware
from app.routers import auth, categories, posts, uploads, root

app = FastAPI(title="FastAPI Blog API")
app.add_middleware(JWTMiddleware)
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(posts.router)
app.include_router(uploads.router)
app.include_router(root.router)

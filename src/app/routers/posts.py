from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.post import PostCreate, PostUpdate, PostOut
from app.services.posts import list_posts, create_post, update_post, soft_delete_post

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[PostOut])
def get_posts(
    db: Session = Depends(get_db),
    page_number: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    category_id: int | None = Query(None),
):
    return list_posts(
        db,
        page_number=page_number,
        page_size=page_size,
        search=search,
        category_id=category_id,
    )


@router.post("/", response_model=PostOut, status_code=201)
def create(payload: PostCreate, db: Session = Depends(get_db)):
    return create_post(
        db,
        title=payload.title,
        content=payload.content,
        category_id=payload.category_id,
        image_url=payload.image_url,
    )


@router.patch("/{post_id}", response_model=PostOut)
def update(post_id: int, payload: PostUpdate, db: Session = Depends(get_db)):
    obj = update_post(db, post_id, data=payload.model_dump())
    if not obj:
        raise HTTPException(404, detail="Post not found")
    return obj


@router.delete("/{post_id}", status_code=204)
def delete(post_id: int, db: Session = Depends(get_db)):
    ok = soft_delete_post(db, post_id)
    if not ok:
        raise HTTPException(404, detail="Post not found")
    return None

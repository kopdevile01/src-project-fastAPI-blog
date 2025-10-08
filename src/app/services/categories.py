from __future__ import annotations
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate


def list_categories(
    db: Session,
    *,
    page_number: int,
    page_size: int,
    search: str | None = None,
) -> list[Category]:
    stmt = select(Category).order_by(Category.id)
    if search:
        stmt = stmt.where(Category.name.ilike(f"%{search}%"))
    offset = (page_number - 1) * page_size
    return db.execute(stmt.offset(offset).limit(page_size)).scalars().all()


def create_category(db: Session, payload: CategoryCreate) -> Category:
    exists = db.scalar(select(Category).where(Category.name == payload.name))
    if exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category already exists",
        )
    obj = Category(name=payload.name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

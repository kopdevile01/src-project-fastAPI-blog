from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category


def get_by_id(db: Session, category_id: int) -> Category | None:
    return db.get(Category, category_id)


def get_by_name(db: Session, name: str) -> Category | None:
    return db.scalar(select(Category).where(Category.name == name))


def db_list(db: Session, *, page_number: int, page_size: int, search: str | None) -> list[Category]:
    stmt = select(Category).order_by(Category.id)
    if search:
        stmt = stmt.where(Category.name.ilike(f"%{search}%"))
    offset = (page_number - 1) * page_size
    return db.execute(stmt.offset(offset).limit(page_size)).scalars().all()


def create(db: Session, *, name: str) -> Category:
    obj = Category(name=name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

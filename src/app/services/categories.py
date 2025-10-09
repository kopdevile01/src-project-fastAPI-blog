from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate
from app.repositories import categories as repo


def list_categories(
    db: Session,
    *,
    page_number: int,
    page_size: int,
    search: str | None = None,
) -> list[Category]:
    return repo.list_(db, page_number=page_number, page_size=page_size, search=search)


def create_category(db: Session, payload: CategoryCreate) -> Category:
    if repo.get_by_name(db, payload.name):
        raise ValueError("Category already exists")
    return repo.create(db, name=payload.name)

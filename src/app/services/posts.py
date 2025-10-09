from __future__ import annotations
from sqlalchemy.orm import Session
from app.repositories import posts as repo
from app.models.post import Post


def list_posts(
    db: Session,
    *,
    page_number: int = 1,
    page_size: int = 10,
    search: str | None = None,
    category_id: int | None = None,
) -> list[Post]:
    return repo.list_(
        db, page_number=page_number, page_size=page_size, search=search, category_id=category_id
    )


def create_post(
    db: Session, *, title: str, content: str, category_id: int, image_url: str | None
) -> Post:
    return repo.create(
        db, title=title, content=content, category_id=category_id, image_url=image_url
    )


def update_post(db: Session, post_id: int, *, data: dict) -> Post | None:
    obj = repo.get(db, post_id)
    if not obj or obj.deleted_at is not None:
        return None
    return repo.update(db, obj, data)


def soft_delete_post(db: Session, post_id: int) -> bool:
    obj = repo.get(db, post_id)
    if not obj or obj.deleted_at is not None:
        return False
    repo.soft_delete(db, obj)
    return True

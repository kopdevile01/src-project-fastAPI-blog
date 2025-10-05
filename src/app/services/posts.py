from __future__ import annotations

from datetime import datetime
from typing import Iterable

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.post import Post


def list_posts(
    db: Session,
    *,
    page_number: int,
    page_size: int,
    search: str | None,
    category_id: int | None,
) -> Iterable[Post]:
    stmt = select(Post).where(Post.deleted_at.is_(None)).order_by(Post.id)

    if category_id is not None:
        stmt = stmt.where(Post.category_id == category_id)

    if search:
        ts = func.to_tsvector(
            "simple",
            func.coalesce(Post.title, "") + func.text(" ") + func.coalesce(Post.content, ""),
        )
        stmt = stmt.where(ts.op("@@")(func.plainto_tsquery("simple", search)))

    offset = (page_number - 1) * page_size
    return db.execute(stmt.offset(offset).limit(page_size)).scalars().all()


def create_post(
    db: Session, *, title: str, content: str, category_id: int, image_url: str | None
) -> Post:
    obj = Post(title=title, content=content, category_id=category_id, image_url=image_url)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_post(db: Session, post_id: int, *, data: dict) -> Post | None:
    obj = db.get(Post, post_id)
    if not obj or obj.deleted_at is not None:
        return None

    for k, v in data.items():
        if v is not None:
            setattr(obj, k, v)

    db.commit()
    db.refresh(obj)
    return obj


def soft_delete_post(db: Session, post_id: int) -> bool:
    obj = db.get(Post, post_id)
    if not obj or obj.deleted_at is not None:
        return False
    obj.deleted_at = datetime.utcnow()
    db.commit()
    return True

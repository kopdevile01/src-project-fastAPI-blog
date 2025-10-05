from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.post import Post


def list_posts(
    db: Session,
    *,
    page_number: int = 1,
    page_size: int = 10,
    search: str | None = None,
    category_id: int | None = None,
) -> list[Post]:
    stmt = select(Post).where(Post.deleted_at.is_(None)).order_by(Post.id)

    if category_id is not None:
        stmt = stmt.where(Post.category_id == category_id)

    if search:
        document = func.to_tsvector("simple", func.concat_ws(" ", Post.title, Post.content))
        query = func.plainto_tsquery("simple", search)
        stmt = stmt.where(document.op("@@")(query))

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
    obj.deleted_at = datetime.now(timezone.utc)
    db.commit()
    return True

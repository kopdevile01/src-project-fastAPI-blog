from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.post import Post


def get(db: Session, post_id: int) -> Post | None:
    return db.get(Post, post_id)


def get_visible(db: Session, post_id: int) -> Post | None:
    stmt = select(Post).where(Post.id == post_id, Post.deleted_at.is_(None))
    return db.scalar(stmt)


def db_list(
    db: Session,
    *,
    page_number: int,
    page_size: int,
    search: str | None,
    category_id: int | None,
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


def create(
    db: Session, *, title: str, content: str, category_id: int, image_url: str | None
) -> Post:
    obj = Post(title=title, content=content, category_id=category_id, image_url=image_url)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_fields(db: Session, obj: Post, data: dict) -> Post:
    for k, v in data.items():
        if v is not None:
            setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def soft_delete(db: Session, obj: Post) -> None:
    obj.deleted_at = datetime.now(timezone.utc)
    db.commit()

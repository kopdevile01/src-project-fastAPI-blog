from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.category import Category


def test_posts_crud_smoke(client, db_session: Session):
    # создадим категорию для FK
    cat = Category(name="Tech")
    db_session.add(cat)
    db_session.commit()
    db_session.refresh(cat)

    # пустой список
    r = client.get("/posts")
    assert r.status_code == 200
    assert r.json() == []

    # create
    payload = {
        "title": "First post",
        "content": "Hello world content",
        "category_id": cat.id,
        "image_url": None,
    }
    r = client.post("/posts", json=payload)
    assert r.status_code == 201
    post_id = r.json()["id"]

    # list
    r = client.get("/posts")
    assert r.status_code == 200
    assert len(r.json()) == 1

    # search (FTS)
    r = client.get("/posts", params={"search": "first"})
    assert r.status_code == 200
    assert len(r.json()) == 1

    # update
    r = client.patch(f"/posts/{post_id}", json={"title": "Updated"})
    assert r.status_code == 200
    assert r.json()["title"] == "Updated"

    # delete (soft)
    r = client.delete(f"/posts/{post_id}")
    assert r.status_code == 204

    r = client.get("/posts")
    assert r.status_code == 200
    assert r.json() == []

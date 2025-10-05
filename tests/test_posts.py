from __future__ import annotations

from sqlalchemy.orm import Session
from app.models.category import Category


def test_posts_crud_smoke(auth_client, client, db_session: Session):
    # подготовка категории
    cat = Category(name="Tech")
    db_session.add(cat)
    db_session.commit()
    db_session.refresh(cat)

    # пустой список (GET публичный)
    r = client.get("/posts")
    assert r.status_code == 200
    assert r.json() == []

    # create (POST защищён)
    payload = {
        "title": "First post",
        "content": "Hello world content",
        "category_id": cat.id,
        "image_url": None,
    }
    r = auth_client.post("/posts", json=payload)
    assert r.status_code == 201
    post_id = r.json()["id"]

    # list (GET публичный)
    r = client.get("/posts")
    assert r.status_code == 200
    assert len(r.json()) == 1

    # search (FTS, GET публичный)
    r = client.get("/posts", params={"search": "first"})
    assert r.status_code == 200
    assert len(r.json()) == 1

    # update (PATCH защищён)
    r = auth_client.patch(f"/posts/{post_id}", json={"title": "Updated"})
    assert r.status_code == 200
    assert r.json()["title"] == "Updated"

    # delete (DELETE защищён, soft delete)
    r = auth_client.delete(f"/posts/{post_id}")
    assert r.status_code == 204

    # после удаления список пуст
    r = client.get("/posts")
    assert r.status_code == 200
    assert r.json() == []

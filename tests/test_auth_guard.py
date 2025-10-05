from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_posts_create_requires_auth():
    r = client.post(
        "/posts/", json={"title": "t", "content": "c", "category_id": 1, "image_url": None}
    )
    assert r.status_code == 401


def test_categories_create_requires_auth():
    r = client.post("/categories", json={"name": "New"})
    assert r.status_code == 401

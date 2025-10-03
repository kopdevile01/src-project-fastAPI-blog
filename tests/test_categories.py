from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_categories_crud_smoke():
    # пустой список
    r = client.get("/categories")
    assert r.status_code == 200
    assert r.json() == []

    # создать
    r = client.post("/categories/", json={"name": "Tech"})
    assert r.status_code == 201
    cat = r.json()
    assert cat["name"] == "Tech"
    assert "id" in cat

    # повтор — конфликт
    r = client.post("/categories/", json={"name": "Tech"})
    assert r.status_code == 409

    # лист с пагинацией
    r = client.get("/categories?page_number=1&page_size=10")
    assert r.status_code == 200
    assert any(c["name"] == "Tech" for c in r.json())

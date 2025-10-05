from __future__ import annotations


def test_categories_crud_smoke(auth_client):
    # пустой список (GET публичный, но можно и auth_client)
    r = auth_client.get("/categories")
    assert r.status_code == 200
    assert r.json() == []

    # создать (POST защищён)
    r = auth_client.post("/categories/", json={"name": "Tech"})
    assert r.status_code == 201
    cat = r.json()
    assert cat["name"] == "Tech"
    assert "id" in cat

    # повтор — должен быть конфликт (тоже защищённый POST, значит auth_client)
    r = auth_client.post("/categories/", json={"name": "Tech"})
    assert r.status_code == 409

    # лист с пагинацией
    r = auth_client.get("/categories?page_number=1&page_size=10")
    assert r.status_code == 200
    assert any(c["name"] == "Tech" for c in r.json())

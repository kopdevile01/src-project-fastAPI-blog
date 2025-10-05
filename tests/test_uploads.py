from fastapi.testclient import TestClient
from app.main import app


def test_upload_image_smoke(monkeypatch, tmp_path):
    def fake_upload_bytes(key: str, data: bytes, content_type: str) -> str:
        assert isinstance(key, str)
        assert isinstance(data, (bytes, bytearray))
        assert content_type in {"image/jpeg", "image/png", "application/octet-stream"}
        return f"http://example.com/blog-images/{key}"

    monkeypatch.setattr("app.routers.uploads.upload_bytes", fake_upload_bytes)

    img = tmp_path / "img.jpg"
    img.write_bytes(b"\xff\xd8\xff\xdb\x00\x43\x00")

    client = TestClient(app)
    with img.open("rb") as fh:
        resp = client.post(
            "/uploads/image",
            files={"file": ("img.jpg", fh, "image/jpeg")},
        )

    assert resp.status_code == 200
    body = resp.json()

    assert body["key"].startswith("images/")
    assert body["key"].endswith(".jpg")
    assert body["url"].endswith(body["key"])

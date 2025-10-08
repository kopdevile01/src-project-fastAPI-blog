from __future__ import annotations

import os
import importlib
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Подменяем БД на тестовую до импорта settings
os.environ["DATABASE_URL"] = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://fastapi_user:fastapi_password@localhost:5432/fastapi_blog_db_test",
)

# Переинициализируем settings, чтобы он прочитал новое DATABASE_URL
import app.core.settings as settings_module

importlib.reload(settings_module)
from app.core.settings import settings  # noqa: E402

from app.db import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402


def _ensure_pg_database_exists(db_url: str) -> None:
    """Создаёт БД, если её нет (через подключение к postgres)."""
    url = make_url(db_url)
    admin_url = url.set(database="postgres")  # подключаемся к системной БД
    dbname = url.database

    engine_admin = create_engine(admin_url, isolation_level="AUTOCOMMIT", future=True)
    with engine_admin.connect() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :n"),
            {"n": dbname},
        ).scalar()
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{dbname}"'))


_ensure_pg_database_exists(settings.database_url)
engine = create_engine(settings.database_url, future=True, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture(scope="session", autouse=True)
def _create_schema():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture()
def db_session():
    conn = engine.connect()
    trans = conn.begin()
    session = TestingSessionLocal(bind=conn)
    try:
        yield session
    finally:
        session.close()
        trans.rollback()
        conn.close()


@pytest.fixture(autouse=True)
def _override_get_db(db_session):
    def _get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_client(client: TestClient) -> TestClient:
    client.post("/auth/register", json={"email": "tester@example.com", "password": "secret"})
    r = client.post("/auth/login", json={"email": "tester@example.com", "password": "secret"})
    assert r.status_code == 200
    return client

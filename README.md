# FastAPI Blog API

Минималистичное API для блога маркетплейса по макетам из Figma.
Стек: FastAPI · SQLAlchemy 2.0 · PostgreSQL · Alembic · JWT (cookies) · Celery/RabbitMQ · S3/MinIO · Pytest · Ruff/Pre-commit · Poetry

## Возможности
- Регистрация + письмо об успешной регистрации через брокер (RabbitMQ) и worker (Celery).
- Логин: выдача JWT, сохранение в cookie, middleware проверяет токен на каждом запросе.
- Категории: список (пагинация + поиск по имени), создание.
- Посты: список (пагинация, фильтр по категории, полнотекстовый поиск на PostgreSQL), создание/изменение, мягкое удаление (soft delete).
- Загрузка изображений в S3/MinIO, возврат публичного URL.
- OpenAPI на `/docs`.

## Репозиторий и layout
- Код в `src/app/...` (src-layout).
- Миграции Alembic — в `migrations/`.

## Требования
- Python **3.12**, Poetry **≥ 2.x**
- Docker + Docker Compose

## Быстрый старт

### Вариант A: локально запускать бекенд, а БД/брокер/S3 в Docker
1) Установи зависимости:
```bash
poetry install
pre-commit install
```
2) Подними зависимости:
```bash
docker compose up -d db rabbitmq minio minio-setup mailhog
```
3) Накати миграции:
```bash
poetry run alembic upgrade head
```
4) Запусти API:
```bash
poetry run uvicorn --app-dir src app.main:app --reload
```

### Вариант B: всё в Docker (включая бекенд и worker)
```bash
docker compose up -d db rabbitmq minio minio-setup mailhog worker backend
```

## Тесты и линтеры
```bash
poetry run ruff check .
poetry run ruff format --check .
poetry run pytest -q
```

## Быстрая проверка
### Регистрация и логин
```bash
curl -s -X POST http://127.0.0.1:8000/auth/register -H 'Content-Type: application/json' \
  -d '{"email":"user@example.com","password":"secret"}'
curl -i -s -X POST http://127.0.0.1:8000/auth/login -H 'Content-Type: application/json' \
  -d '{"email":"user@example.com","password":"secret"}'
```
### Список категорий
```bash
curl -s "http://127.0.0.1:8000/categories?page_number=1&page_size=10"
```
### Загрузка изображения (если поднят MinIO)
```bash
curl -s -F "file=@$HOME/Загрузки/1.jpg;type=image/jpeg" http://127.0.0.1:8000/uploads/image
```
### OpenAPI
http://127.0.0.1:8000/docs

### Полезные ссылки (локально)

MailHog UI (инбокс писем): http://127.0.0.1:8025

MinIO Console: http://127.0.0.1:9001 (логин/пароль по умолчанию в .env/compose)

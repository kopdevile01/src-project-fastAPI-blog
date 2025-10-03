# ---------- Vars ----------
PY = poetry run
UVICORN = uvicorn --app-dir src app.main:app

# ---------- Dev ----------
.PHONY: install
install:           ## Установить зависимости (prod+dev)
	poetry install --no-interaction --no-ansi

.PHONY: pre-commit-install
pre-commit-install: ## Установка git-хуков pre-commit
	$(PY) pre-commit install

.PHONY: lint
lint:              ## Проверить стиль (ruff)
	$(PY) ruff check .
	$(PY) ruff format --check .

.PHONY: fmt
fmt:               ## Отформатировать код (ruff format)
	$(PY) ruff format .

.PHONY: test
test:              ## Запустить тесты
	$(PY) pytest -q

.PHONY: run
run:               ## Локальный запуск API (без Docker backend)
	$(PY) $(UVICORN) --reload

# ---------- Docker ----------
.PHONY: up-db
up-db:             ## Поднять только Postgres и RabbitMQ
	docker compose up -d db rabbitmq

.PHONY: up
up:                ## Поднять всё (db, rabbitmq, backend)
	docker compose up -d

.PHONY: down
down:              ## Остановить и удалить контейнеры/сеть/тома (без named volumes)
	docker compose down

.PHONY: logs
logs:              ## Логи backend
	docker compose logs -f backend

.PHONY: db-shell
db-shell:          ## Открыть psql в контейнере БД
	docker compose exec db psql -U fastapi_user -d fastapi_blog_db

# ---------- Clean ----------
.PHONY: clean
clean:             ## Удалить кеши Python/pytest/ruff
	find . -name '__pycache__' -type d -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache

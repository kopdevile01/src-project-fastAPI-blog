from __future__ import annotations

from celery import Celery

from app.core.settings import settings

celery = Celery(
    "app",
    broker=settings.rabbitmq_url,
    backend=None,
)

celery.conf.task_always_eager = bool(settings.test_database_url)
celery.conf.task_ignore_result = True

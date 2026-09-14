# app/worker/celery_app.py

from app.core.logging_config import setup_logging

setup_logging()

from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "medvision",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    task_track_started=True,
    worker_pool="threads",
    worker_concurrency=3,
)

celery_app.autodiscover_tasks(["app.worker"])